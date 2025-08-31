from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import BusinessTokenObtainPairView, MeView


urlpatterns = [
    path('auth/login/', BusinessTokenObtainPairView.as_view(), name='business-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='business-token-refresh'),
    path('auth/me/', MeView.as_view(), name='business-me'),
]


