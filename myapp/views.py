from django.shortcuts import render, redirect
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum
# Create your views here.


def index(request):
    expense_form = ExpenseForm()

    if request.method == "POST":
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()

    expenses = Expense.objects.all()
    total_expenses = expenses.aggregate(Sum('amount'))
    context = {
        'expense_form': expense_form,
        'expenses': expenses,
        'total_expenses': total_expenses
    }
    return render(request, 'myapp/index.html', context)


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


def delete(request, id):
    if request.method == 'POST' and 'delete' in request.POST:
        expense = Expense.objects.get(id=id)
        expense.delete()

    return redirect('index')
