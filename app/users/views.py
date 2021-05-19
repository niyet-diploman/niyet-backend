from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import MyUserSerializer, PasswordResetsSerializer, ResetPasswordSerializer
from .models import MyUser, PasswordResets
from django.http import Http404
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.mail import send_mail
import hashlib
import time
import datetime


class MyUsersAPIView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MyUserSerializer

    def get_queryset(self):
        return MyUser.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class ForgotPasswordAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetsSerializer

    def get_user(self, email):
        try:
            user = MyUser.objects.get(username=email)
        except MyUser.DoesNotExist:
            raise Http404
        return user

    def perform_create(self, serializer):
        email = self.request.data.get('email')
        user = self.get_user(email=email)
        hash = hashlib.sha1()
        hash.update("{}{}".format(user.email, time.time()).encode("utf-8"))
        code = hash.hexdigest()
        # sender = settings.EMAIL_HOST_USER
        # send_mail("Сброс пароля", "Ваша ссылка для сброса пароля: http:://localhost:3000/auth/forgot-password/{}"
        #           .format(code), sender, [email], fail_silently=False)
        serializer.save(email=email, code=code, user=user)


class ResetPasswordAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

    def perform_create(self, serializer):
        code = self.kwargs.get('code')
        if code is not None:
            try:
                password_reset = PasswordResets.objects.get(code=code)
                created_at = password_reset.created_at
                now = datetime.datetime.now()
                difference = now - created_at.replace(tzinfo=None)
                expire_time = settings.RESET_PASSWORD_EXPIRE
                if expire_time - difference.total_seconds() > 0:
                    user = password_reset.user
                    user.set_password(self.request.data.get('password'))
                    user.save()
                    password_reset.delete()
                else:
                    password_reset.delete()
                    raise Http404
            except PasswordResets.DoesNotExist:
                raise Http404
        else:
            raise Http404


class UserAPIView(APIView):

    def get_user(self, pk):
        try:
            user = MyUser.objects.get(id=pk)
        except MyUser.DoesNotExist:
            raise Http404
        return user

    def get(self, request):
        if request.user.is_authenticated:
            serializer = MyUserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            exception = {"detail": "Authentication credentials were not provided."}
            return Response(exception, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        if request.user.is_authenticated:
            serializer = MyUserSerializer(request.user)
            user = self.get_user(pk=request.user.id)
            password = self.request.data.get('password', None)
            if password is None or len(password) == 0:
                request.data['password'] = user.password
            serializer.update(instance=user, validated_data=request.data)
            return Response(status=status.HTTP_200_OK)
        else:
            exception = {"detail": "Authentication credentials were not provided."}
            return Response(exception, status=status.HTTP_401_UNAUTHORIZED)

