from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import *
from django.contrib import messages
# Create your views here.
def index(request):
    exists = UserPreference.objects.filter(user = request.user).exists()
    user_prefernces = None
    currencies = []
    file_path = os.path.join(settings.BASE_DIR,'currencies.json')
    # import pdb
    # pdb.set_trace()
    with open(file_path,'r') as file:
        data = json.load(file)
        for k,v in data.items():
            currencies.append({'name':k,'value':v})
    if exists:
        user_prefernces = UserPreference.objects.get(user= request.user)

    if request.method=='GET':
        return render(request,'preferences/index.html',{'currencies':currencies,'user_preferences':user_prefernces})
    else:
        currency = request.POST['currency']
        if exists:
            user_prefernces.currency = currency
            user_prefernces.save()
        else:
            UserPreference.objects.create(user=request.user,currency=currency)
        messages.success(request,'Changes saved')
        return render(request,'preferences/index.html',{'currencies':currencies,'user_preferences':user_prefernces})



