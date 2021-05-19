from rest_framework.routers import DefaultRouter
from app.donations.views import *
from django.urls import path, include

router = DefaultRouter()

router.register(r'beneficiaries', BeneficiaryViewSet, basename='beneficiaries')
router.register(r'donations', DonationViewSet, basename='donations')
router.register(r'payments', PaymentViewSet, basename='payments')
router.register(r'programs', ProgramViewSet, basename='programs')
router.register(r'default-amounts', DefaultDonationAmountViewSet, basename='amounts')
router.register(r'beneficiaryAmount', BeneficiaryAmountViewSet, basename='beneficiaryAmount')

urlpatterns = [
    path('zakyat-calculate/', ZakyatCalculationAPIView.as_view(), name='zakyat_calculate')
]

urlpatterns += router.urls
