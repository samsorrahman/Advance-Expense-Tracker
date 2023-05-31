from django.shortcuts import render
from .forms import ExpenseForm
# Create your views here.


def index(request):
    expense_form = ExpenseForm()

    if request.method == "POST":
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()

    context = {
        'expense_form': expense_form,
    }
    return render(request, 'myapp/index.html', context)
