from app.users.models import *
from app.utility.models import *
from django.db import models
from .enums import *
from ..utility.enums import *
import uuid
# from django.contrib.postgres.fields import ArrayField
# import requests
# from json2xml import json2xml
# from json2xml.utils import readfromurl, readfromstring, readfromjson


class Program(TimestampMixin):
    title = models.CharField(max_length=255, null=False)
    text = models.TextField(null=False)
    icon = models.ImageField(upload_to='program_images', default=None, null=True, blank=True)
    icon2 = models.ImageField(upload_to='program_images', default=None, null=True, blank=True)
    poster = models.ImageField(upload_to='program_images', default=None, null=True, blank=True)

    class Meta:
        verbose_name = 'Program'
        verbose_name_plural = 'Programs'


class Beneficary(TimestampMixin):
    gender_status = models.IntegerField(choices=BeneficiariesGenderStatus.choices(), null=False)
    anonym_status = models.IntegerField(choices=BeneficiariesAnonymStatus.choices(), null=False)
    social_status = models.IntegerField(choices=BeneficiariesSocialStatus.choices(), null=False)
    # donation_state = models.IntegerField(choices=BeneficiariesDonationState.choices(), null=False)
    city = models.ForeignKey(City, null=True, blank=True, default=None, on_delete=models.DO_NOTHING)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    birthday = models.DateField(null=False)
    age = models.IntegerField(null=False, default=0)
    last_payment_day = models.DateTimeField(null=True, blank=True, default=None)
    payment_count = models.IntegerField(null=False, default=0)
    parents = models.TextField(null=True, blank=True, default=None)
    address = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=255, null=False)
    characteristics = models.TextField(null=True, default=None)
    program = models.ForeignKey(Program, null=False, default=None, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Beneficary'
        verbose_name_plural = 'Beneficaries'


class BeneficiaryAmount(TimestampMixin):
    beneficiary = models.ForeignKey(Beneficary, null=False, on_delete=models.DO_NOTHING)
    certificate_amount = models.FloatField(null=False)
    def __str__(self):
        return 'beneficiary: {}, certificate_amount: {}'.format(self.beneficiary, self.certificate_amount)


class Donation(TimestampMixin):
    donor = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING, null=True, default=None)
    program = models.ForeignKey(Program, on_delete=models.DO_NOTHING, null=False)
    beneficiaries = models.ManyToManyField(BeneficiaryAmount, related_name='beneficiaries', null=True)
    donation_amount = models.FloatField(null=True)
    certificate_amount = models.FloatField(null=True)
    donation_status = models.IntegerField(choices=DonationState.choices(), default=DonationState.PENDING.value,
                                          null=False)
    donation_anonymous_state = models.IntegerField(choices=DonorAnonymStatus.choices(),
                                                   default=DonorAnonymStatus.PUBLIC.value, null=False)
    donation_type = models.IntegerField(choices=DonationType.choices(), default=DonationType.COMMON.value,
                                        null=False)
    guest = models.BooleanField(default=False)
    donation_automatic = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'

    def __str__(self):
        return 'donor {}, program {}, beneficiaries {}'.format(self.donor, self.program, self.beneficiaries)



class DonorRecurringProfile(TimestampMixin):
    donor = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING)
    recurring_period = models.IntegerField(choices=DonorRecurringPeriod.choices(), null=False)
    recurring_profile_id = models.IntegerField(null=False)
    amount = models.IntegerField(null=False)
    recurring_period_expire_date = models.CharField(max_length=255, default=None)
    active_status = models.IntegerField(null=False)
    in_processing = models.IntegerField(default=None)
    last_transaction = models.TimeField(null=True, default=None)
    next_transaction = models.TimeField(null=True, default=None)

    class Meta:
        verbose_name = 'Donor recurring profile'
        verbose_name_plural = 'Donor recurring profiles'


class Payment(TimestampMixin):
    order_id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4, editable=False,
                                primary_key=True)
    amount = models.FloatField(default=0, null=False)
    donation = models.OneToOneField(Donation, on_delete=models.DO_NOTHING, null=True)
    title = models.CharField(max_length = 255, null=True, default= "Пожертвование")
    payment_description = models.CharField(default='Пожертвование', max_length=255)
    payment_url = models.TextField(null=True, default=' ')
    payment_result_url = models.TextField(null=True, default=' ')
    payment_id_paybox = models.CharField(default='0', max_length=255)
    payment_status = models.IntegerField(choices=PaymentStatus.choices(), null=False,
                                         default=PaymentStatus.CREATED_PAYMENT.value)
    payment_paybox_result = models.CharField(max_length=255, default="none", null=True)
    payment_date = models.CharField(max_length=255, default="", null=True)
    payment_signature = models.CharField(max_length=255, default="", null=True)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'


class PartnerProgram(TimestampMixin):
    partner = models.ForeignKey(Partner, null=False, on_delete=models.DO_NOTHING, default=1)
    city = models.ForeignKey(City, null=False, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)

    class Meta:
        verbose_name = 'Partner program'
        verbose_name_plural = 'Partner programs'


class Certificate(TimestampMixin):
    beneficiary = models.ForeignKey(Beneficary, on_delete=models.DO_NOTHING)
    program = models.CharField(max_length=255, null=True)
    amount = models.FloatField(null=True)
    partner_program = models.ForeignKey(PartnerProgram, on_delete=models.DO_NOTHING, null=True)
    donation = models.ForeignKey(Donation, on_delete=models.DO_NOTHING)
    issued_state = models.IntegerField(choices=IssueState.choices(), default=IssueState.CREATED.value)
    # issued_by = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING)
    # donor_anonymous_status = models.IntegerField(choices=DonorAnonymStatus.choices(),
    #                                              default=DonorAnonymStatus.PUBLIC.value)
    comment = models.TextField(null=True)
    # issue_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Certificate'
        verbose_name_plural = 'Certificates'


class Gift(TimestampMixin):
    partner_program = models.ForeignKey(PartnerProgram, null=True, on_delete=models.DO_NOTHING)
    beneficiary = models.ForeignKey(Beneficary, on_delete=models.DO_NOTHING)
    gift_counts = models.IntegerField(null=True)
    comment = models.TextField(null=False)
    gift_image = models.ImageField(upload_to='gift_images', null=True)

    class Meta:
        verbose_name = 'Gift'
        verbose_name_plural = 'Gifts'


class DefaultDonationAmount(TimestampMixin):
    sum = models.IntegerField(null=False)

    class Meta:
        verbose_name = 'Default donation denominations'
        verbose_name_plural = 'Default donation denominations'
