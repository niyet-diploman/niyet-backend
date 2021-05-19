from .models import *
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostSubscription
        fields = '__all__'


class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = '__all__'


class VideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class GoldPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoldPrice
        fields = '__all__'


class PrincipleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Principle
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class WidgetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widgets
        fields = '__all__'


class VolunteersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteers
        fields = '__all__'


class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = '__all__'


class VolunteerRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerRequests
        fields = '__all__'
