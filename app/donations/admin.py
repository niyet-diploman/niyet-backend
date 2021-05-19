from django.contrib import admin
from .models import *


@admin.register(Beneficary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'birthday', 'city', 'gender_status', 'anonym_status',
                    'social_status',  'last_payment_day', 'payment_count', 'parents', 'address',
                    'phone', 'characteristics')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('id', 'beneficiary', 'program', 'issued_state', 'comment', 'created_at')


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('id', 'donor', 'program', 'donation_amount', 'donation_status', 'donation_anonymous_state')


@admin.register(DonorRecurringProfile)
class DonorRecurringProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'donor', 'recurring_period', 'recurring_profile_id', 'amount', 'recurring_period_expire_date',
                    'active_status', 'in_processing', 'last_transaction', 'next_transaction')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'payment_status', 'amount', 'donation', 'payment_description')


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'poster')


@admin.register(PartnerProgram)
class PartnerProgramAdmin(admin.ModelAdmin):
    list_display = ('id', 'partner', 'city', 'title', 'description')


@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    list_display = ('id', 'partner_program', 'beneficiary', 'gift_counts', 'comment')

# @admin.register(BeneficiaryAmountArray)
# class BeneficiaryAmountArrayAdmin(admin.ModelAdmin):
#     list_display = ('id','beneficiaries_array')


@admin.register(BeneficiaryAmount)
class BeneficiaryAmountArrayAdmin(admin.ModelAdmin):
    list_display = ('id', 'beneficiary', 'certificate_amount')


@admin.register(DefaultDonationAmount)
class DefaultDonationAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'sum')
