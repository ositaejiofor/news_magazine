from django.db import models

class Donation(models.Model):
    email = models.EmailField(blank=True, null=True)  # Stripe may send customer email
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # stored in $
    stripe_payment_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"${self.amount} from {self.email or 'Anonymous'}"
