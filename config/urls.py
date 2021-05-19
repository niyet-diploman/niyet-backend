from django.conf import settings
from django.contrib import admin
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path, re_path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
   openapi.Info(
      title="Niyet API",
      default_version='v1',
      description="NIyet",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="kumar.akhmadiyev@gmail.com"),
      license=openapi.License(name="PRIVATE"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('utility/', include('app.utility.urls')),
    path('auth/', include('app.users.urls')),
    path('', include('app.donations.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        re_path(
            r'swagger(?P<format>\.json|\.yaml)',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'
        ),
        path(
            'docs/',
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'
        ),
    ]
