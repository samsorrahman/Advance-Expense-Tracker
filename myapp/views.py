from django.shortcuts import render
from .forms import ExpenseForm
from .models import Expense
# Create your views here.


def index(request):
    expense_form = ExpenseForm()

    if request.method == "POST":
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()

    expenses = Expense.objects.all()
    context = {
        'expense_form': expense_form,
        'expenses': expenses,

    }
    return render(request, 'myapp/index.html', context)
