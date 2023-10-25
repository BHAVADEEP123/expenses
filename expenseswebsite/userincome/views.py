from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
import json
import datetime
# Create your views here.


@login_required(login_url='/authentication/login')
def index(request):
    IncomeData = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(IncomeData,per_page=4)
    page_number = request.GET.get('page')
    pagedata = paginator.get_page(page_number)
    context={
        'IncomeData':IncomeData,
        'pagedata':pagedata
    }
    # import pdb
    # pdb.set_trace()
    return render(request,'income/index.html',context)

def search_data(request):
    if request.method=='POST':
        txt = json.loads(request.body).get('search_text')
        
        print("text :"+ txt)
        # expenses = Expense.objects.filter(owner = request.user)
        incomes = UserIncome.objects.filter(amount__istartswith=txt, owner=request.user) | UserIncome.objects.filter(date__istartswith=txt, owner=request.user) | UserIncome.objects.filter(source__icontains=txt, owner=request.user) | UserIncome.objects.filter(description__icontains=txt, owner=request.user)
        data = incomes.values()
        return JsonResponse(list(data),safe=False)


def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources':sources,
    }
    if request.method == "GET":
        
        return render(request, 'income/add_income.html',context)

    if request.method=="POST":

        context['values']=request.POST
        amount = request.POST['amount']
        # description = request.POST['description']
        # import pdb
        # pdb.set_trace()
        if amount=='':
            messages.warning(request,"Amount field can't be empty")
            return render(request,'income/add_income.html',context)
        descreption = request.POST['description']
        source = request.POST['source']
        date = request.POST['date']
        # import pdb
        # pdb.set_trace()
        if not descreption:
            messages.warning(request,"Description cant be emtpy")
            return render(request,'income/add_income.html',context)
        if not source:
            messages.warning(request,"Please choose a source")
            return render(request,'income/add_income.html',context)
        if date:
            new_expense = UserIncome.objects.create(owner = request.user,amount = amount, description = descreption, source = source, date = date)
            new_expense.save()
        else:
            new_expense = UserIncome.objects.create(owner = request.user,amount = amount, description = descreption, source = source)
            new_expense.save()
            
        messages.success(request,"Income added successfully")
        return redirect('income')
    
def income_edit(request,id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income':income,
        'values':income,
        'sources':sources
    }
    if request.method == "GET":
        return render(request,'income/edit-income.html',context)
    else:
        # context['values']=request.POST
        amount = request.POST['amount']
        # description = request.POST['description']
        # import pdb
        # pdb.set_trace()
        if amount=='':
            messages.warning(request,"Amount field can't be empty")
            return render(request,'income/edit-income.html',context)
        descreption = request.POST['description']
        source = request.POST['source']
        date = request.POST['date']
        # import pdb
        # pdb.set_trace()
        if not descreption:
            messages.warning(request,"Description cant be emtpy")
            return render(request,'income/edit-income.html',context)
        if not source:
            messages.warning(request,"Please choose a category")
            return render(request,'income/edit-income.html',context)
        if date:
            income.owner = request.user
            income.amount = amount
            income.description = descreption
            income.source = source
            income.date = date
            income.save()
        else:
            income.owner = request.user
            income.amount = amount
            income.description = descreption
            income.source = source
            income.save()
            
        messages.success(request,"Income updated successfully")
        return redirect('income')
        # messages.info(request,"Handling post form")
        
        # return render(request,"expenses/edit-expense.html",context)

def income_delete(request,id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request,"Income deleted successfully")
    return redirect('income')

def income_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    incomes = UserIncome.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_category(income):
        return income.source
    category_list = list(set(map(get_category, incomes)))

    def get_income_category_amount(category):
        amount = 0
        filtered_by_category = incomes.filter(source=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in incomes:
        for y in category_list:
            finalrep[y] = get_income_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def stats_view(request):
    return render(request, 'income/stats.html')