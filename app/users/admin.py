from django.contrib import admin
from .models import *


@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'second_name', 'role', 'pay_zakyat')


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'description')


@admin.register(PasswordResets)
class PasswordResetsAdmin(admin.ModelAdmin):
    list_display = ('email', 'user', 'code', 'created_at',)
