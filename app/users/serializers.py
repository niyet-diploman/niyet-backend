from rest_framework import serializers
from .models import MyUser, PasswordResets


class MyUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=255, required=False)
    second_name = serializers.CharField(max_length=255, required=False)
    pay_zakyat = serializers.BooleanField(required=True)
    email = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = MyUser
        fields = ('id', 'email', 'password', 'first_name', 'second_name', 'pay_zakyat')

    def create(self, validated_data):

        user = MyUser.objects.create(
            username=validated_data.get('email', None),
            email=validated_data.get('email', None),
            first_name=validated_data.get('first_name', None),
            second_name=validated_data.get('second_name', None),
            pay_zakyat=validated_data.get('pay_zakyat', None)
        )
        user.set_password(validated_data.get('password', None))
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('email', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.second_name = validated_data.get('second_name', instance.second_name)
        instance.pay_zakyat = validated_data.get('pay_zakyat', instance.pay_zakyat)
        password = validated_data.get('password', None)
        new_password = validated_data.get('new_password', None)
        if password is not None and instance.check_password(password) and new_password is not None\
                and len(new_password) > 0:
            instance.set_password(new_password)
        instance.save()
        return instance


    # def validate_username(self, value):
    #     if not len(value) >= 5:
    #         raise serializers.ValidationError("Username should contain more than 4 symbols")
    #     return value


class PasswordResetsSerializer(serializers.ModelSerializer):
    code = serializers.CharField(write_only=True, required=False)
    user = MyUserSerializer(write_only=True, required=False)

    class Meta:
        model = PasswordResets
        fields = '__all__'


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, required=True)
