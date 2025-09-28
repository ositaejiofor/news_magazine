from django.contrib import admin
from .models import Donation

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("email", "amount", "stripe_payment_id", "created_at")
    search_fields = ("email", "stripe_payment_id")
