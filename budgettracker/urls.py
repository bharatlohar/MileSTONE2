from django.urls import path,include
from .import views
from rest_framework.routers import DefaultRouter
from .views import (UserViewSet,UserProfileViewSet,InputSaveViewSet,CategoryViewSet,IncomeViewSet,ExpenseViewSet,BudgetViewSet,EMIViewSet)
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet)
router.register(r'input-saves', InputSaveViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'incomes', IncomeViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'budgets', BudgetViewSet)
router.register(r'emis', EMIViewSet)

urlpatterns = [
    path('',views.functionname,name='home'),
    path('', include(router.urls)),
]
