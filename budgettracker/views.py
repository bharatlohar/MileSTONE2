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
)
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.mail import send_mail
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.core.mail import send_mail
from decimal import Decimal
from .utils import send_alert
from rest_framework.decorators import action



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
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=False, methods=['get'])
    def check_budget_alerts(self, request):
        alerts = []
        budgets = Budget.objects.filter(user=request.user)
        expenses = Expense.objects.filter(user=request.user).values('category').annotate(total=Sum('amount'))


        for budget in budgets:
            for expense in expenses:
                if expense['category'] == budget.category.id and expense['total'] > budget.limit:
                    alerts.append(f"Alert: You have exceeded your budget for {budget.category.name}.")
                    print(f"Sending exceeded alert to {request.user.email}")
                    send_alert(request.user, budget.category, exceeded=True)  # Sending alert if exceeded
                elif expense['category'] == budget.category.id and expense['total'] >= budget.limit * Decimal("0.9"):
                    alerts.append(f"Warning: You are nearing your budget for {budget.category.name}.")
                    print(f"Sending exceeded alert to {request.user.email}")
                    send_alert(request.user, budget.category, exceeded=False)  # Sending alert if nearing


        return Response({"alerts": alerts})


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

class login(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

class ReportView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        # Optionally get a specific date from the request query parameters
        date = request.query_params.get('date')  # Format: YYYY-MM-DD

        if date:
            # Filter expenses by date
            expenses = Expense.objects.filter(user=request.user, date=date)
        else:
            # Get all expenses for the user if no date is provided
            expenses = Expense.objects.filter(user=request.user)

        total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Prepare detailed report data
        report_data = {
            'total_expense': total_expense,
            'details': expenses.values('category__name').annotate(total=Sum('amount')),
        }
        return Response(report_data)

    @action(detail=False, methods=['get'])
    def generate_pdf(self, request):
        date = request.query_params.get('date')  # Optional date filter
        
        if date:
            expenses = Expense.objects.filter(user=request.user, date=date)
        else:
            expenses = Expense.objects.filter(user=request.user)

        total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

        # Create a PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        p = canvas.Canvas(response, pagesize=letter)

        # Draw the report content
        p.drawString(100, 750, "Expense Report")
        p.drawString(100, 730, f"Date Filter: {date if date else 'All Dates'}")
        p.drawString(100, 710, f"Total Expense: {total_expense}")
        
        # Draw category-wise expense details
        y_position = 690
        for expense in expenses.values('category__name').annotate(total=Sum('amount')):
            p.drawString(100, y_position, f"Category: {expense['category__name']}, Amount: {expense['total']}")
            y_position -= 20
        
        p.showPage()
        p.save()
        return response
    
class ChartDataView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        
        # Total income and expense over time (for line chart)
        income_data = Income.objects.filter(user=user).values('date').annotate(total=Sum('amount'))
        expense_data = Expense.objects.filter(user=user).values('date').annotate(total=Sum('amount'))

        # Budget utilization by category (for bar chart)
        budget_data = Budget.objects.filter(user=user).values('category__name').annotate(limit=Sum('limit'))
        expense_by_category = Expense.objects.filter(user=user).values('category__name').annotate(total=Sum('amount'))

        # Category-wise spending (for pie chart)
        category_spending = Expense.objects.filter(user=user).values('category__name').annotate(total=Sum('amount'))

        return Response({
            'income_data': income_data,
            'expense_data': expense_data,
            'budget_data': budget_data,
            'expense_by_category': expense_by_category,
            'category_spending': category_spending,
        })