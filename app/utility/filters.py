from django_filters import rest_framework as filters
from app.utility.models import TimestampMixin, Post, Question, PostSubscription


class TimeStampMixinFilter(filters.FilterSet):
    start_time = filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    end_time = filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = TimestampMixin
        fields = ['start_time', 'end_time']


class PostFilter(filters.FilterSet):
    post_type = filters.CharFilter(lookup_expr='iexact')
    start_time = filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    end_time = filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = Post
        fields = ['post_type', 'start_time', 'end_time']


class PostSubscriptionFilter(filters.FilterSet):
    email = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = PostSubscription
        fields = ['email']


class QuestionFilter(filters.FilterSet):
    email = filters.CharFilter(lookup_expr='iexact')
    start_time = filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    end_time = filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = Question
        fields = ['email', 'start_time', 'end_time']
