# authentication/urls.py

from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token-refresh'),
    path('register/', views.RegisterView.as_view(), name='register')
]