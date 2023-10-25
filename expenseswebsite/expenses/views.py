import csv
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference
import datetime
# Create your views here.


@login_required(login_url='/authentication/login')
def index(request):
    expensesData = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expensesData,per_page=4)
    page_number = request.GET.get('page')
    pagedata = paginator.get_page(page_number)
    context={
        'expensesData':expensesData,
        'pagedata':pagedata
    }
    # import pdb
    # pdb.set_trace()
    return render(request,'expenses/index.html',context)

def search_data(request):
    if request.method=='POST':
        txt = json.loads(request.body).get('search_text')
        
        print("text :"+ txt)
        # expenses = Expense.objects.filter(owner = request.user)
        expenses = Expense.objects.filter(amount__istartswith=txt, owner=request.user) | Expense.objects.filter(date__istartswith=txt, owner=request.user) | Expense.objects.filter(category__icontains=txt, owner=request.user) | Expense.objects.filter(description__icontains=txt, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data),safe=False)


def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories':categories,
    }
    if request.method == "GET":
        
        return render(request, 'expenses/add_expense.html',context)

    if request.method=="POST":

        context['values']=request.POST
        amount = request.POST['amount']
        # description = request.POST['description']
        # import pdb
        # pdb.set_trace()
        if amount=='':
            messages.warning(request,"Amount field can't be empty")
            return render(request,'expenses/add_expense.html',context)
        descreption = request.POST['description']
        categroy = request.POST['category']
        date = request.POST['date']
        # import pdb
        # pdb.set_trace()
        if not descreption:
            messages.warning(request,"Description cant be emtpy")
            return render(request,'expenses/add_expense.html',context)
        if not categroy:
            messages.warning(request,"Please choose a category")
            return render(request,'expenses/add_expense.html',context)
        if date:
            new_expense = Expense.objects.create(owner = request.user,amount = amount, description = descreption, category = categroy, date = date)
            new_expense.save()
        else:
            new_expense = Expense.objects.create(owner = request.user,amount = amount, description = descreption, category = categroy)
            new_expense.save()
            
        messages.success(request,"Expense added successfully")
        return redirect('expenses')
    
def expense_edit(request,id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense':expense,
        'values':expense,
        'categories':categories
    }
    if request.method == "GET":
        return render(request,'expenses/edit-expense.html',context)
    else:
        # context['values']=request.POST
        amount = request.POST['amount']
        # description = request.POST['description']
        # import pdb
        # pdb.set_trace()
        if amount=='':
            messages.warning(request,"Amount field can't be empty")
            return render(request,'expenses/edit-expense.html',context)
        descreption = request.POST['description']
        categroy = request.POST['category']
        date = request.POST['date']
        # import pdb
        # pdb.set_trace()
        if not descreption:
            messages.warning(request,"Description cant be emtpy")
            return render(request,'expenses/edit-expense.html',context)
        if not categroy:
            messages.warning(request,"Please choose a category")
            return render(request,'expenses/edit-expense.html',context)
        if date:
            expense.owner = request.user
            expense.amount = amount
            expense.description = descreption
            expense.category = categroy
            expense.date = date
            expense.save()
        else:
            expense.owner = request.user
            expense.amount = amount
            expense.description = descreption
            expense.category = categroy
            expense.save()
            
        messages.success(request,"Expense updated successfully")
        return redirect('expenses')
        # messages.info(request,"Handling post form")
        
        # return render(request,"expenses/edit-expense.html",context)

def expense_delete(request,id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request,"Expense deleted successfully")
    return redirect('expenses')

def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def stats_view(request):
    return render(request, 'expenses/stats.html')

def export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename = expenses'+\
        str(datetime.datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(["Amount","Description","Category","Date"])
    expenses = Expense.objects.filter(owner = request.user)
    for expense in expenses:
        writer.writerow([expense.amount,expense.description,expense.category,expense.date])
    return response