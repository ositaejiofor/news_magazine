from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime
import stripe

from .models import Donation

stripe.api_key = settings.STRIPE_SECRET_KEY


# -----------------------------
# Donation Page
# -----------------------------
def donate_view(request):
    """Render the donation page"""
    context = {"stripe_public_key": settings.STRIPE_PUBLIC_KEY}
    return render(request, "donate/donate.html", context)


# -----------------------------
# Create Stripe Checkout Session
# -----------------------------
@csrf_exempt
def create_checkout_session(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        amount = float(request.POST.get("amount", 0))
        if amount < 1:
            raise ValueError("Amount must be at least $1")
        amount_cents = int(amount * 100)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": "Donation"},
                "unit_amount": amount_cents,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=request.build_absolute_uri("/donate/success/"),
        cancel_url=request.build_absolute_uri("/donate/cancel/"),
    )
    return JsonResponse({"id": session.id})



# -----------------------------
# Stripe Webhook
# -----------------------------
@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Handle Stripe webhook events for one-time and recurring donations"""
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET  # set in .env

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    # Handle completed payments or subscriptions
    if event["type"] in ["checkout.session.completed", "invoice.payment_succeeded"]:
        session = event["data"]["object"]

        # Extract customer info and amount
        if event["type"] == "checkout.session.completed":
            customer_email = session.get("customer_details", {}).get("email")
            amount_total = session.get("amount_total", 0) / 100
            payment_id = session.get("payment_intent")
        else:  # recurring subscription payment
            customer_email = session.get("customer_email")
            amount_total = session.get("amount_paid", 0) / 100
            payment_id = session.get("id")

        # Save donation in DB
        donation, created = Donation.objects.get_or_create(
            stripe_payment_id=payment_id,
            defaults={"email": customer_email, "amount": amount_total},
        )

        # Send thank-you email
        if created and customer_email:
            subject = "Thank You for Your Donation ❤️"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [customer_email]

            text_content = f"Dear supporter,\n\nThank you for your donation of ${amount_total:.2f}.\nYour support makes a real difference.\n\n- Your Organization"

            html_content = render_to_string("emails/thank_you.html", {
                "amount": f"{amount_total:.2f}",
                "year": datetime.now().year
            })

            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=True)

    return HttpResponse(status=200)
