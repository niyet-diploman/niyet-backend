from django.contrib import admin
from .models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('post_type', 'title', 'text', 'author', 'poster', 'created_at', 'updated_at')


@admin.register(PostSubscription)
class PostSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribe', 'token')


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'author', 'poster', 'enabled')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'poster')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('donation_state', 'state', 'title')


@admin.register(GoldPrice)
class GoldPriceAdmin(admin.ModelAdmin):
    list_display = ('gram_in_kzt',)


@admin.register(Principle)
class PrincipleAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'number', 'author', 'poster')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_status', 'email', 'message')


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Widgets)
class WidgetsAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'poster')


@admin.register(Volunteers)
class VolunteersAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'poster')


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('title', 'file', 'author')


@admin.register(VolunteerRequests)
class VolunteerRequestsAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'phone')
