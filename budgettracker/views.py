# budgettracker/views.py
from urllib import response
from django.shortcuts import render
from rest_framework import viewsets, status  # Import 'status' here
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken  # Import ObtainAuthToken
from rest_framework.authtoken.models import Token  # Import Token model for token management
from django.contrib.auth import login, logout  # Import login and logout functions
from django.contrib.auth.decorators import login_required
from .models import User, UserProfile, InputSave, Category, Income, Expense, Budget, EMI
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    InputSaveSerializer,
    CategorySerializer,
    IncomeSerializer,
    ExpenseSerializer,
    BudgetSerializer,
    EMISerializer,
    UserLoginSerializer  # Import UserLoginSerializer
)
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce


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

class UserLoginView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)  # Log the user in
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can log out

    def post(self, request):
        logout(request)  # Log the user out
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


