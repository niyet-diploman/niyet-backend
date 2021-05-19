from .serializers import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin,\
    DestroyModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from app.utility.filters import *
from rest_framework.decorators import action
from app.donations.filters import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests
from lxml import etree
import hashlib
from .models import *
from .paybox_client import Paybox
import math


class PaymentViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,
                     GenericViewSet):
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    filterset_class = TimeStampMixinFilter

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentGETSerializer
        if self.action == "create":
            return PaymentPOSTSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            donor = self.request.user
            donation = Donation.objects.filter(donor=donor)
            return Payment.objects.filter(donation__in=donation)
        else:
            return None

    def perform_create(self, serializer):
        donation_id = self.request.data.get('donation')
        donation = Donation.objects.get(id=donation_id)
        serializer.save(amount=donation.donation_amount)


    @action(methods=['POST'], detail=True)
    def paybox(self, request, pk):
        p = Paybox()
        payment = Payment.objects.get(order_id=pk)
        order = pk
        amount = payment.amount
        description = payment.payment_description

        response = p.paybox_request(order, amount, description)
        # print(response.content)
        root = etree.fromstring(response.content)
        # print(root.find('pg_payment_id').text)
        payment.payment_id_paybox = root.find('pg_payment_id').text
        payment.payment_url = root.find('pg_redirect_url').text
        payment.payment_signature = root.find('pg_sig').text

        payment.payment_status = PaymentStatus.PAYMENT_PENDING_PAYBOX.value
        payment.save()



        return Response(response)


    @action(methods=['POST'], detail=True)
    def payment_result(self, request, pk):
        payment = Payment.objects.get(order_id=pk)
        beneficiaries = Beneficary.objects.all()

        data = request.data
        result = data.get('pg_result')

        if result is 1:
            donation = payment.donation
            print(donation)
            beneficiary_amounts = donation.beneficiaries.all() # [1]
            print(beneficiary_amounts)

            for b in beneficiary_amounts:
                beneficiary_id = b.beneficiary.id
                beneficiary = beneficiaries.get(id=beneficiary_id)
                beneficiary.payment_count+=1
                beneficiary.last_payment_day = datetime.datetime.now()
                beneficiary.save()
            return Response("OK")
        else:
            return Response("ERROR")


class BeneficiaryViewSet(ListModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = BeneficarySerializer
    pagination_class = PageNumberPagination
    filterset_class = BeneficiaryFilter

    def get_queryset(self):
        user = self.request.user
        if user.pay_zakyat is not None and user.pay_zakyat is True:
            return Beneficary.objects.order_by('payment_count', 'last_payment_day').filter(age__lt=12)
        return Beneficary.objects.order_by('payment_count', 'last_payment_day')

    def perform_update(self, serializer):
        serializer.save()


class DonorRecurringProfileViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_classes = DonorRecurringProfileSerializer
    queryset = DonorRecurringProfile.objects.all()

    def perform_create(self, serializer):
        serializer.save(donor=self.request.user)


class ProgramViewSet(ListModelMixin, GenericViewSet):
    permission_classes = (AllowAny, )
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()


class BeneficiaryAmountViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated, )
    def get_serializer_class(self):
        if self.action == "list":
            return BeneficiaryAmountGETSerializer
        if self.action == "create":
            return BeneficiaryAmountPOSTSerializer

    def get_queryset(self):
        return BeneficiaryAmount.objects.all()


class DonationViewSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == "list":
            return DonationGETSerializer
        if self.action == "create":
            return DonationPOSTSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            donor = self.request.user
            return Donation.objects.filter(donor=donor)
        return Donation.objects.all()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(donor=self.request.user)
            if self.request.data.get('donation_automatic'):
                donation_amount = self.request.data.get('donation_amount')
                certificate_amount = self.request.data.get('certificate_amount')
                beneficiary_amount = donation_amount / certificate_amount
                beneficiaries = Beneficary.objects.all()[:beneficiary_amount]
                donation_beneficiaries = []
                for b in beneficiaries:
                    bb = BeneficiaryAmount(beneficiary=b, certificate_amount=certificate_amount)
                    bb.save()
                    donation_beneficiaries.append(bb)
                serializer.save(beneficiaries=donation_beneficiaries)
            else:
                amount = 0
                # BeneficiaryAmount должен создаться
                beneficiaries = self.request.data.get('beneficiaries')
                for b in beneficiaries:
                    bb = BeneficiaryAmount.objects.get(id=b)
                    amount += bb.certificate_amount
                    serializer.save(donation_amount=amount)
        else:
            serializer.save(guest=True)
            serializer.save(donation_anonymous_state=DonorAnonymStatus.ANONYM.value)
            # serializer.save(donation_amount=self.request.data.get('donation_amount'))
            # serializer.save(certificate_amount = self.request.data.get('certificate_amount'))
            donation_amount = self.request.data.get('donation_amount')
            certificate_amount = self.request.data.get('certificate_amount')
            beneficiary_amount = donation_amount / certificate_amount
            beneficiaries = Beneficary.objects.all()[:beneficiary_amount]
            donation_beneficiaries = []
            for b in beneficiaries:
                bb = BeneficiaryAmount(beneficiary=b, certificate_amount=certificate_amount)
                bb.save()
                donation_beneficiaries.append(bb)
            serializer.save(beneficiaries=donation_beneficiaries)


class DefaultDonationAmountViewSet(ListModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = DefaultDonationAmountSerializer

    def get_queryset(self):
        return DefaultDonationAmount.objects.all()


class ZakyatCalculationAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        nisab = 0
        overall_sum = 0
        zakyat_sum = 0
        if GoldPrice.objects.count() > 0:
            last_price = GoldPrice.objects.last()
            price = last_price.gram_in_kzt
            nisab = price * 85
        else:
            exception = {"message": "Gold price not found"}
            return Response(exception, status=status.HTTP_404_NOT_FOUND)
        cash = request.data.get('cash', 0)
        in_bank_money = request.data.get('in_bank_money', 0)
        gold_and_silver = request.data.get('gold_and_silver', 0)
        securities = request.data.get('securities', 0)
        products = request.data.get('products', 0)
        other_incomes = request.data.get('other_incomes', 0)
        solid_minerals = request.data.get('solid_minerals', 0)
        fluid_minerals = request.data.get('fluid_minerals', 0)
        debts = request.data.get('debts', 0)
        expenses = request.data.get('expenses', 0)

        cash_actives = cash + in_bank_money + gold_and_silver + securities + products + other_incomes
        minerals = solid_minerals + fluid_minerals
        actives = cash_actives + minerals - debts - expenses
        if actives > nisab:
            actives_zakyat = cash_actives * 0.025
            minerals_zakyat = fluid_minerals * 0.025 + solid_minerals * 0.2
            zakyat_sum += actives_zakyat + minerals_zakyat
            overall_sum += cash_actives + fluid_minerals + solid_minerals
        # should take out debts and expenses?

        harvest_amount = request.data.get('harvest_amount', 0)
        harvest_cost = request.data.get('harvest_cost', 0)
        irrigation_type = request.data.get('irrigation_type', None)

        if harvest_amount > 675:
            percentage = 0.05
            if irrigation_type == 'natural':
                percentage = 0.1
            zakyat_sum += harvest_cost * harvest_amount * percentage
            overall_sum += harvest_cost * harvest_amount

        sheep_amount = request.data.get('sheep_amount', 0)
        sheep_cost = request.data.get('sheep_cost', 0)
        cow_amount = request.data.get('cow_amount', 0)
        cow_cost = request.data.get('cow_cost', 0)
        camel_amount = request.data.get('camel_amount', 0)
        camel_cost = request.data.get('camel_cost', 0)

        if sheep_amount >= 40:
            if 40 <= sheep_amount <= 120:
                zakyat_sum += sheep_cost

            if 120 < sheep_amount <= 200:
                zakyat_sum += 2 * sheep_cost

            if 200 < sheep_amount <= 399:
                zakyat_sum += 3 * sheep_cost

            if 399 < sheep_amount <= 499:
                zakyat_sum += 4 * sheep_cost

            if sheep_amount > 499:
                zakyat_sum += math.ceil(sheep_amount / 100) * sheep_cost

        if cow_amount >= 30:
            if 30 <= cow_amount < 40:
                zakyat_sum += cow_cost

            if 40 <= cow_amount < 60:
                zakyat_sum += cow_cost

            if 60 <= cow_amount < 70:
                zakyat_sum += 2 * cow_cost

            if 70 <= cow_amount < 80:
                zakyat_sum += 2 * cow_cost

            if 80 <= cow_amount < 90:
                zakyat_sum += 2 * cow_cost

            if 90 <= cow_amount < 100:
                zakyat_sum += 3 * cow_cost

            if 100 <= cow_amount < 110:
                zakyat_sum += 3 * cow_cost

            if 110 <= cow_amount < 120:
                zakyat_sum += 3 * cow_cost

            if 120 <= cow_amount < 130:
                zakyat_sum += 4 * cow_cost

            if cow_amount >= 130:
                zakyat_sum += math.ceil(cow_amount / 30) * cow_cost

        if camel_amount >= 5:
            if 5 <= camel_amount < 10:
                zakyat_sum += sheep_cost

            if 10 <= camel_amount < 15:
                zakyat_sum += 2 * sheep_cost

            if 15 <= camel_amount < 20:
                zakyat_sum += 3 * sheep_cost

            if 20 <= camel_amount < 25:
                zakyat_sum += 4 * sheep_cost

            if 25 <= camel_amount < 36:
                zakyat_sum += camel_cost

            if 36 <= camel_amount < 46:
                zakyat_sum += camel_cost

            if 46 <= camel_amount < 61:
                zakyat_sum += camel_cost

            if 61 <= camel_amount < 76:
                zakyat_sum += camel_cost

            if 76 <= camel_amount < 91:
                zakyat_sum += 2 * camel_cost

            if 91 <= camel_amount < 121:
                zakyat_sum += 2 * camel_cost

            if camel_amount >= 121:
                zakyat_sum += math.ceil(camel_amount / 30) * camel_cost

        overall_sum += sheep_cost * sheep_amount
        overall_sum += cow_cost * cow_amount
        overall_sum += camel_cost * camel_amount
        result = {"zakyat_sum": math.floor(zakyat_sum), "overall_sum": math.floor(overall_sum)}
        return Response(result, status=status.HTTP_200_OK)

