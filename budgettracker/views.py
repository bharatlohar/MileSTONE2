# budgettracker/views.py
from urllib import response
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, viewsets
from .models import User, UserProfile, InputSave, Category, Income, Expense, Budget, EMI
from .serializers import (UserSerializer,UserProfileSerializer,InputSaveSerializer,CategorySerializer,IncomeSerializer,ExpenseSerializer,BudgetSerializer,EMISerializer
)
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required

# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# UserProfile ViewSet
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

# InputSave ViewSet
class InputSaveViewSet(viewsets.ModelViewSet):
    queryset = InputSave.objects.all()
    serializer_class = InputSaveSerializer
    permission_classes = [IsAuthenticated]

# Category ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

# Income ViewSet
class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

# Expense ViewSet
class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

# Budget ViewSet
class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

# EMI ViewSet
class EMIViewSet(viewsets.ModelViewSet):
    queryset = EMI.objects.all()
    serializer_class = EMISerializer
    permission_classes = [IsAuthenticated]


def functionname(request):
    return render(request, 'home/index.html')

def login(request):
    return render(request, 'registration/login.html')

class DashboardView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        # Retrieve the total income for the logged-in user
        total_income = Income.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Retrieve the total expenses for the logged-in user
        total_expense = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Retrieve the count of EMIs for the logged-in user
        ems_count = EMI.objects.filter(user=request.user).count()

        # Summarize expenses by category
        category_summary = Expense.objects.filter(user=request.user) \
            .values('category__name') \
            .annotate(total=Sum('amount'))

        return Response({
            'total_income': total_income,
            'total_expense': total_expense,
            'ems_count': ems_count,
            'category_summary': category_summary,
        })
    
@login_required  # Ensure user is authenticated
def profile_view(request):
    return render(request, 'profile.html')  # Ensure this template exists

def Dashboard_view(request):
    return render(request, 'dashboard.html')