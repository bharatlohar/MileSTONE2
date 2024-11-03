# budgettracker/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Dashboard_view, login, profile_view
from .views import (
    UserViewSet, UserProfileViewSet, InputSaveViewSet, 
    CategoryViewSet, IncomeViewSet, ExpenseViewSet, 
    BudgetViewSet, EMIViewSet, functionname
)
from django.contrib.auth import views as auth_views

# Create a router and register the ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet)
router.register(r'input-saves', InputSaveViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'incomes', IncomeViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'budgets', BudgetViewSet)
router.register(r'emis', EMIViewSet)

# URL patterns
urlpatterns = [
    path('', functionname, name='home'),  # Basic view to render the homepage
    path('', include(router.urls)),  
    path('dashboard/', Dashboard_view, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    
]