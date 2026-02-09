from django.urls import  path, include
from rest_framework.routers import DefaultRouter
from .views import SessionsViewSet

router = DefaultRouter()
router.register(r'sessions', SessionsViewSet)

urlpatterns = [
    path('', include(router.urls),)
]