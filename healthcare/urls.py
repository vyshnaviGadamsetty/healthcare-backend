"""
URL configuration for healthcare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import PatientViewSet, DoctorViewSet, PatientDoctorViewSet, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'mappings', PatientDoctorViewSet, basename='mapping')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('', include(router.urls)),
        path('auth/register/', RegisterView.as_view(), name='register'),
        path('auth/login/', TokenObtainPairView.as_view(), name='login'),
        path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ])),
]
