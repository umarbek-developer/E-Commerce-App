from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AddressViewSet, ChangePasswordView, LoginView, LogoutView, MeView, RegisterView

router = DefaultRouter()
router.register(r'addresses', AddressViewSet, basename='address')
router.include_root_view = False

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
    path('me/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('', include(router.urls)),
]
