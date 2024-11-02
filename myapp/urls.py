"""
URL configuration for myapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from budgettracker.views import DashboardView

# Configure the Swagger UI schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Budget Tracker System API",
        default_version='v1',
        description="API documentation for the Grievance Handling System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@grievance.local"),
        license=openapi.License(name="Budget Tracker"),
          ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('budgettracker/', include('budgettracker.urls')),  # Include your app's URLs 
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
     path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
     path('dashboard/', DashboardView.as_view({'get': 'list'}), name='dashboard'),
]