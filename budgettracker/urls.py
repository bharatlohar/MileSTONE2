# budgettracker/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, UserProfileViewSet, InputSaveViewSet, 
    CategoryViewSet, IncomeViewSet, ExpenseViewSet, 
    BudgetViewSet, EMIViewSet, functionname
)

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
    path('', include(router.urls)),      # Include all the routes from the router
]
