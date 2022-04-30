from base64 import urlsafe_b64decode, urlsafe_b64encode
from datetime import datetime
from email import message
import email
from lib2to3.pgen2.tokenize import generate_tokens
from urllib import request
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from exercise.models import user
from wholeness import settings
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from . tokens import generate_token
from formtools.wizard.views import SessionWizardView
import uuid
from .models import user
from django.conf import settings
from subprocess import run, PIPE
import sys



# Create your views here.
def index(request):
    return render(request,"Exercise/index.html")

def home(request,user=''):
    
    # dob=user.dob
    # age=datetime.today-dob
    # gender=user.gender
    context={ "age":50,  "gender":'female'}
   


    return render(request,"Exercise/home.html",context)

def register(request):
    if request.method=="POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        gender=request.POST['gender']
        dob=request.POST['dob']
        height=request.POST['height']
        weight=request.POST['weight']
        
        name= fname+" " +lname

        my_user=user(name=name,gender=gender,dob=dob,height=height,weight=weight,email=email)
        #user_obj=User.objects.create_user(name=fname+" "+lname,gender=gender,dob=dob,height=height,weight=weight,email=email)
        my_user.is_verified =False
        my_user.save()
        messages.success(request,"your details had been stored succesfully")
        
        messages.success(request,"before email sent")
        send_mail_verify(request,my_user,email,name)
        messages.success(request,"we have sent an e-mail please check")
        return redirect('success')

        
        
    return render(request,'Exercise/register.html')
    

def send_mail_verify(request,my_user,email,name):
    subject ="Welcome"
    message =f'hii {name} \nThank you for joining wholeness '
    email_from =settings.EMAIL_HOST_USER
    recipent_list=[email]
    send_mail(subject,message,email_from,recipent_list)
    current_site=get_current_site(request)
    email_subject="confirm your email !!"
    message2 =render_to_string('email_confirmation.html',{
        'name': name,
        'domain':current_site.domain,
        'uid': urlsafe_b64encode(force_bytes(my_user.pk)),
        'token':generate_token.make_token(my_user)
    })
    E_mail=EmailMessage(email_subject,message2,settings.EMAIL_HOST_USER,recipent_list)
    E_mail.send()

def activate(request,uidb64,token):
    
    try:
        uid=force_str(urlsafe_b64decode(uidb64))
        my_user =user.objects.get(pk=uid)

    except(TypeError,ValueError,OverflowError,user.DoesNotExist):
        my_user=None
    
    if my_user is not None and generate_token.check_token(my_user,token):
        my_user.is_verified=True
        print("hii")
        my_user.save()
        return redirect('account',my_user)
    
    else:
        return render(request,'Exercise/signup.html')


def account(request,my_user):
    if request.method=="POST":
        username=request.POST['username']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if user.objects.filter(username==username):
            messages.error(request,"username is already exist! please try another username ")
            return redirect(' account ')
        if pass1!=pass2:
            messages.error(request," password doesn't match")
            return redirect ('account')

        my_user.username=username
        my_user.password=pass1
        my_user.pass2=pass2
        my_user.save()
        return redirect('login')
    return redirect("account")


def login(request):
    
    if request.method=="POST":
        username=request.POST['username']
        pass1=request.POST['pass1']
        #return redirect('home')

        user=authenticate(username=username,password=pass1)

        if user is not None:
            login(request,user)
            fname=user.first_name
            return redirect('home',user)
            #return render(request,"Exercise/home.html", {'fname':fname})
        else:
            messages.error(request,"Invalid Credtials")
            return redirect('login')

    return render(request,"Exercise/login.html")




def workout(request):
    return render(request,'Exercise/workoutpage.html')

def profile(request):
    return render(request,'Exercise/profilepage.html')

def diseases(request):
    return render(request,'diseases/diseasemainpage.html')

def food(request):
    return render(request,'Exercise/foodpage.html')

def setting(request):
    return render(request,'Exercise/settingspage.html')

def error(request):
    return render(request,'Exercise/error.html')

def success(request):
    return render(request,"Exercise/success.html")

def exercise(request):
    
    return render(request,"Exercise/exercisepage.html")

def external(request):
    out=run([sys.executable,'D:\wholeness\wholeness\exercise\pushup.py'],shell=False,stdout=PIPE)
    print(out)
    return render(request,"Exercise/exercisepage.html")


def logout(request):
    logout(request)
    messages.success(request,"Logged out Successfully!")
    return redirect('index')
