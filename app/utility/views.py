from app.utility.serializers import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from app.utility.models import *
from app.utility.filters import *


class PostViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filterset_class = PostFilter


class PostSubscriptionViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = PostSubscriptionSerializer
    queryset = PostSubscription.objects.all()
    filterset_class = PostSubscriptionFilter


class SlideViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = SlideSerializer
    pagination_class = PageNumberPagination
    queryset = Slide.objects.filter(enabled=True)
    filterset_class = TimeStampMixinFilter


class VideosViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = VideosSerializer
    pagination_class = PageNumberPagination
    queryset = Video.objects.all()
    filterset_class = TimeStampMixinFilter


class CityViewSet(ListModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CitySerializer
    queryset = City.objects.all()


class GoldPriceView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        if GoldPrice.objects.count() > 0:
            last_price = GoldPrice.objects.last()
            price = last_price.gram_in_kzt
            nisab = price * 85
            return Response({'gram_in_kzt': price, 'nisab': nisab}, status=status.HTTP_200_OK)
        else:
            exception = {"message": "Gold price not found"}
            return Response(exception, status=status.HTTP_404_NOT_FOUND)


class PrincipleViewSet(ListModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = PrincipleSerializer
    queryset = Principle.objects.all()


class QuestionViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    filterset_class = TimeStampMixinFilter


class StoreViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,
                   GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = StoreSerializer
    pagination_class = PageNumberPagination
    queryset = Store.objects.all()
    filterset_class = TimeStampMixinFilter


class WidgetsViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = WidgetsSerializer
    queryset = Widgets.objects.all()


class VolunteersViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = VolunteersSerializer
    pagination_class = PageNumberPagination
    queryset = Volunteers.objects.all()
    filterset_class = TimeStampMixinFilter


class StatisticsViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = StatisticsSerializer
    queryset = Statistics.objects.all()


class VolunteersRequestViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = VolunteerRequestsSerializer
    queryset = VolunteerRequests.objects.all()
