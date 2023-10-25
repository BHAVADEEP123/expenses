from collections.abc import Callable, Iterable, Mapping
from typing import Any
from django.shortcuts import render,redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
import re

from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False


def is_weak_password(password):
    # Minimum length requirement
    if len(password) < 8:
        return True
    
    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return True
    
    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return True
    
    # Check for at least one digit
    if not re.search(r'\d', password):
        return True
    
    # Check for at least one special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return True
    
    # Password is strong
    return False

class EmailThread(threading.Thread):
    def __init__(self,email):
        self.email = email
        threading.Thread.__init__(self)
    def run(self):
        self.email.send(fail_silently=False)

# Create your views here.
class RegistrationView(View):
    def get(self,request):
        return render(request,'authentication/register.html')
    
    def post(self,request):
        # get User data
        # validate
        # create user

        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        context = {
            "fieldValues":request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if(len(password)<6):
                    print("password too short")
                    messages.warning(request,"Password too short")
                    return render(request,'authentication/register.html',context)
                user = User.objects.create_user(username=username,email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                
                uibd64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse("activate",kwargs={'uibd64':uibd64,'token':token_generator.make_token(user)})
                email_subject = "Activate your account"
                active_url = "http://"+domain+link
                email_body = "Hi "+user.username+", Please use the below link to verify your account\n"+active_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    "noreply@semycolon.com",
                    [email],
                )
                EmailThread(email).start()
                messages.success(request,"registration successful")
                return render(request,'authentication/register.html')

        return render(request,'authentication/register.html')
    
class VerificationView(View):
    def get(self,request,uibd64,token):
        try:
            id = force_str(urlsafe_base64_decode(uibd64))
            user = User.objects.get(pk=id) 
            if not token_generator.check_token(user,token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request,"Account activated successfully") 
            return redirect('login')

        except Exception as ex:
            pass
        return redirect('login')
    
class LoginView(View):
    def get(self,request):
        return render(request,'authentication/login.html')
    
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = auth.authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request,"Welcome "+username)
                    return redirect('expenses')
                messages.warning(request,"Account is not active. Please check your mail and activate it")
                return render(request,'authentication/login.html')
            messages.warning(request,"Invalid Credentials")
            return render(request,'authentication/login.html')
        messages.warning(request,"Please fill all the fields")
        return render(request,'authentication/login.html')

class LogoutView(View):
    def post(self,request):
        auth.logout(request)
        messages.success(request,'logged out succesfully')
        return redirect('login')

class UserNameValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should contain only alpha-numeric charecters'},status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'username taken'},status=409)
        
        
        return JsonResponse({'username_valid':True})


class PasswordStrengthView(View):
    def post(self,request):
        
        
        # requestBody = re.sub(r'(\r\n|\n)','',str(request.body))
        # print("data retrieved: "+requestBody)
        print('data:'+request.body.decode())
        data = json.loads(request.body.decode())

        password = data['password']
        if(is_weak_password(str(password))):
            return JsonResponse({'weak':True},status=410)
        return JsonResponse({'strong':True},status=411)
        
class EmailValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        email = data['email']
        if not is_valid_email(str(email)):
            return JsonResponse({'email_error':'not a valid email'},status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'email under use'},status=409)
        
        
        return JsonResponse({'email_valid':True})

class RequestPasswordResetEmail(View):
    def get(self,request):
        return render(request,'authentication/reset-password.html')
    
    def post(self,request):
        email = request.POST['email']
        context = {
            'fieldValues':request.POST
        }
        if not is_valid_email(email):
            messages.warning(request,'Not a valid email')
            return render(request,'authentication/reset-password.html',context)
        userr = User.objects.filter(email=email)
        if userr.exists():
            user = userr[0]
            domain = get_current_site(request).domain
            uibd64 = urlsafe_base64_encode(force_bytes(user.pk))
            link = reverse("reset-user-password",kwargs={'uibd64':uibd64,'token':PasswordResetTokenGenerator().make_token(user)})
            email_subject = "Password Reset"
            active_url = "http://"+domain+link
            email_body = "Hi "+user.username+", Please use the below link to reset password for your account\n"+active_url
            email = EmailMessage(
                email_subject,
                email_body,
                "noreply@semycolon.com",
                [email],
            )
            EmailThread(email).start()
            
        messages.success(request,"A link has been sent to the registered email to reset your password")
        

        return render(request,'authentication/reset-password.html')
    
class CompletePasswordReset(View):
    def get(self,request,uibd64,token):
        context={
            'uibd64':uibd64,
            'token':token
        }
        user_id = force_str(urlsafe_base64_decode(uibd64))
        user = User.objects.get(pk=user_id)
        if not PasswordResetTokenGenerator().check_token(user,token):
            messages.info(request,"This link has been already used!!")
            return render(request,'authentication/login.html')
        return render(request,'authentication/set-newpassword.html',context)
    def post(self,request,uibd64,token):
        context={
            'uibd64':uibd64,
            'token':token
        }
        password = request.POST['password']
        if len(password)<=6:
            messages.warning(request,"password is too short")
            return render(request,'authentication/set-newpassword.html',context)
        user_id = force_str(urlsafe_base64_decode(uibd64))
        user = User.objects.get(pk=user_id)
        user.set_password(password)
        user.save()
        messages.success(request,"Password reset done successfully")
        return redirect('login')
        return render(request,'authentication/set-newpassword.html',context)