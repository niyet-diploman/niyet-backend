from rest_framework.routers import DefaultRouter
from app.utility.views import *
from django.urls import path, include
router = DefaultRouter()

router.register(r'posts', PostViewSet, basename='posts')
router.register(r'post-subscriptions', PostSubscriptionViewSet, basename='post_subscriptions')
router.register(r'slides', SlideViewSet, basename='slides')
router.register(r'videos', VideosViewSet, basename='videos')
router.register(r'cities', CityViewSet, basename='cities')
router.register(r'principles', PrincipleViewSet, basename='principles')
router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'stores', StoreViewSet, basename='stores')
router.register(r'widgets', WidgetsViewSet, basename='widgets')
router.register(r'volunteers', VolunteersViewSet, basename='volunteers')
router.register(r'statistics', StatisticsViewSet, basename='statistics')
router.register(r'volunteer-requests', VolunteersRequestViewSet, basename='volunteer_requests')

urlpatterns = [
    path('gold-price/', GoldPriceView.as_view(), name='gold_price')
]

urlpatterns += router.urls
