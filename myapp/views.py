from django.shortcuts import render, redirect
from .forms import ExpenseForm
from .models import Expense
import datetime
from django.db.models import Sum
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.


@login_required(login_url='login')
def index(request):
    expense_form = ExpenseForm()

    if request.method == "POST":
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.instance.user = request.user
            expense.save()

    expenses = Expense.objects.filter(user=request.user)
    total_expenses = expenses.aggregate(Sum('amount'))

    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data = expenses.filter(date__gt=last_year)
    yearly_sum = data.aggregate(Sum('amount'))

    last_month = datetime.date.today() - datetime.timedelta(days=30)
    data = expenses.filter(date__gt=last_month)
    monthly_sum = data.aggregate(Sum('amount'))

    last_week = datetime.date.today() - datetime.timedelta(days=7)
    data = expenses.filter(date__gt=last_week)
    weekly_sum = data.aggregate(Sum('amount'))

    daily_sums = expenses.values('date').order_by(
        'date').annotate(sum=Sum('amount'))

    categorical_sums = expenses.values('category').order_by(
        'category').annotate(sum=Sum('amount'))

    context = {
        'expense_form': expense_form,
        'expenses': expenses,
        'total_expenses': total_expenses,
        'yearly_sum': yearly_sum,
        'monthly_sum': monthly_sum,
        'weekly_sum': weekly_sum,
        'daily_sums': daily_sums,
        'categorical_sums': categorical_sums,
    }
    return render(request, 'myapp/index.html', context)


@login_required(login_url='login')
def edit(request, id):
    expense = Expense.objects.get(id=id)
    expense_form = ExpenseForm(instance=expense)

    if request.method == 'POST':
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {
        'expense_form': expense_form,
    }

    return render(request, 'myapp/edit.html', context)


@login_required(login_url='login')
def delete(request, id):
    if request.method == 'POST' and 'delete' in request.POST:
        expense = Expense.objects.get(id=id)
        expense.delete()

    return redirect('index')


def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')


def registerUser(request):
    if request.method == 'POST':
        # Retrieve the form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            # Passwords do not match, handle the error (e.g., show an error message)
            # You can redirect to the registration page or display an error message
            messages.error(request, 'Password does not match!')
            return redirect('register')

        # Create the user
        user = User.objects.create_user(
            username=username, password=password, email=email, first_name=name)

        # You can also set additional fields if needed, such as user profile or extra information

        # Save the user to the database
        user.save()

        # Redirect to a success page or login page
        return redirect('index')

    # Render the registration template if the request method is not POST
    page = 'register'
    context = {
        'page': page
    }
    return render(request, 'myapp/registration.html', context)


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Username Or password is incorrect')
    return render(request, 'myapp/registration.html')
