from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.urls import path


schema_view = get_schema_view(
    openapi.Info(
        title='Blogs DRF',
        default_version='v1',
        description='Add your posts with our DRF',
        contact=openapi.Contact(url='https://www.linkedin.com/in/liana-kalpakchyan-622a49198/')
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
