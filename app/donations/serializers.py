from .models import *
from rest_framework import serializers
from app.utility.serializers import *


class DonorRecurringProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonorRecurringProfile
        fields = '__all__'


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'


class BeneficarySerializer(serializers.ModelSerializer):
    city = CitySerializer(required=False)
    program = ProgramSerializer(required=True)

    class Meta:
        model = Beneficary
        fields = '__all__'


class BeneficiaryAmountGETSerializer(serializers.ModelSerializer):
    beneficiary = BeneficarySerializer(required=True)

    class Meta:
        model = BeneficiaryAmount
        fields = '__all__'

class BeneficiaryAmountPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeneficiaryAmount
        fields = '__all__'

class DonationGETSerializer(serializers.ModelSerializer):
    program = ProgramSerializer(required=False)
    beneficiaries = BeneficiaryAmountGETSerializer(required=True, many=True)

    class Meta:
        model = Donation
        fields = ['id','donation_amount', 'program', 'beneficiaries']

class DonationPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['id','program', 'beneficiaries']


class PaymentGETSerializer(serializers.ModelSerializer):
    donation = DonationPOSTSerializer(required=False)

    class Meta:
        model = Payment
        fields = '__all__'


class PaymentPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['issued_state', 'comment', 'city', 'beneficiary', 'program', 'donation']


# class BeneficiaryAmountArraySerializer(serializers.ModelSerializer):
#     beneficiaries_array = BeneficiaryAmountSerializer
#     class Meta:
#         model = BeneficiaryAmountArray
#         fields = '__all__'



class DefaultDonationAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultDonationAmount
        fields = '__all__'
