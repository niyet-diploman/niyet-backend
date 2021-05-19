from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from .views import MyUsersAPIView, ForgotPasswordAPIView, ResetPasswordAPIView, UserAPIView

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('register/', MyUsersAPIView.as_view()),
    path('users/', MyUsersAPIView.as_view()),
    path('me/', UserAPIView.as_view()),
    path('forgot-password/', ForgotPasswordAPIView.as_view()),
    path('reset-password/<code>/', ResetPasswordAPIView.as_view())
]
