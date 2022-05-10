from base64 import urlsafe_b64decode, urlsafe_b64encode
from datetime import datetime,date,timedelta
from email import message
import email
from lib2to3.pgen2.tokenize import generate_tokens
from urllib import request
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from exercise.models import user_login,user_detail
from wholeness import settings
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from . tokens import generate_token
from formtools.wizard.views import SessionWizardView
import uuid
from .models import user_detail,user_login
from django.conf import settings
from subprocess import run, PIPE
import sys
from dateutil.relativedelta import relativedelta
from .models import week_weight
from .utils import get_plot


# Create your views here.
def index(request):
    return render(request,"Exercise/index.html")


def home(request,user=''):
    dob= user_detail.objects.all()[0].dob
    gender= user_detail.objects.all()[0].gender
    
    # dob=user.Dob
    age=date.today()-dob
    
    # print(age- relativedelta(years=years)/365)
    seconds_in_year = 365.25*24*60*60
    age=int(age.total_seconds() / seconds_in_year)
    # gender=user.Gender
    context={ "age":age,  "gender":gender}
    # context={ }
    # context["user"] = user_detail.objects.all()

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

        my_user=user_detail(name=name,gender=gender,dob=dob,height=height,weight=weight,email=email)
        #user_obj=User.objects.create_user(name=fname+" "+lname,gender=gender,dob=dob,height=height,weight=weight,email=email)
        my_user.is_verified =False
        my_user.save()
        messages.success(request,"your details had been stored succesfully")
        
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
        my_user =user_detail.objects.get(pk=uid)

    except(TypeError,ValueError,OverflowError,user_detail.DoesNotExist):
        my_user=None
    
    if my_user is not None and generate_token.check_token(my_user,token):
        my_user.is_verified=True
        print("hii")
        my_user.save()
        return redirect('account')
    
    else:
        return render(request,'Exercise/signup.html')


def account(request):
    if request.method=="POST":
        username=request.POST['username']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        my_user=user_login(username=username,password=pass1)

        if user_login.objects.filter(username==username):
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

        user=user_login(username=username,password=pass1)

        if user is not None:
            login(request,user)
            fname=user.first_name
            return redirect('home',user)
            #return render(request,"Exercise/home.html", {'fname':fname})
        else:
            messages.error(request,"Invalid Credtials")
            return redirect('login')

    return render(request,"Exercise/login.html")

def main_view(request):
  if request.method=="POST":
    week=request.POST['week']
    weight=request.POST['weight']
  
    data=week_weight(week=week,weight=weight)

    data.save()

    return redirect('graph')

  return render(request,'Exercise/profilepage.html')

def graph(request):

  qs = week_weight.objects.all()
  x=[x.week for x in qs]
  y=[y.weight for y in qs]
  chart = get_plot(x,y)
  return render(request,'Exercise/profilepage.html',{'chart': chart})


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

def pushup(request):
    
    return render(request,"Exercise/pushups.html")

def planks(request):
    
    return render(request,"Exercise/planks.html")

def external_pushups(request):
    out=run([sys.executable,'D:\wholeness\wholeness\exercise\pushup.py'],shell=False,stdout=PIPE)
    print(out)
    return render(request,"Exercise/pushups.html")

def external_planks(request):
    out=run([sys.executable,'D:\wholeness\wholeness\exercise\plank.py'],shell=False,stdout=PIPE)
    print(out)
    return render(request,"Exercise/planks.html")

def veglunch(request):
    return render(request,"Exercise/vlunch.html")

def nonveglunch(request):
    return render(request,"Exercise/nvlunch.html")

def nonvegbreak(request):
    return render(request,"Exercise/nvbfast.html")

def nonvegsnacks(request):
    return render(request,"Exercise/nvevng.html")

def nonvegdinner(request):
    return render(request,"Exercise/nvdinner.html")

def veg(request):
    return render(request,"Exercise/vbled.html")

def non_veg(request):
    return render(request,"Exercise/nvbled.html")



def heart(request):
    return render(request,'diseases/heartdis.html')

def bladder(request):
    return render(request,'diseases/bladderdis.html')

def digestive(request):
    return render(request,'diseases/digestivedis.html')

def femrep(request):
    return render(request,'diseases/femalereproductivesystemdis.html')

def kidney(request):
    return render(request,'diseases/kidneysdis.html')

def liver(request):
    return render(request,'diseases/liverdis.html')

def malrep(request):
    return render(request,'diseases/malereproductivesystemdis.html')

def pancreases(request):
    return render(request,'diseases/pancreasesdis.html')

def respiratory(request):
    return render(request,'diseases/respiratorydis.html')



def Logout(request):
    logout(request)
    messages.success(request,"Logged out Successfully!")
    return redirect('index')
