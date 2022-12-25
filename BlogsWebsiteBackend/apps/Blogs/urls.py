from django.urls import path, include
from .views import (
    PostViewset,
    CategoryViewset
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('posts', PostViewset)
router.register('categories', CategoryViewset)

urlpatterns = [
    path('', include(router.urls)),
]
