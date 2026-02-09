from django.urls import  path, include
from rest_framework.routers import DefaultRouter
from .views import SessionsViewSet, login_view, signup_view

router = DefaultRouter()
router.register(r'sessions', SessionsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
]
