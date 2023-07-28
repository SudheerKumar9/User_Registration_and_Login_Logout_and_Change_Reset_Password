from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from app.forms import *
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required




def registration(request):
    USFO=UserForm()
    PFO=ProfileForm()
    d={'USFO':USFO,'PFO':PFO}
    if request.method=='POST' and request.FILES:
        USFD=UserForm(request.POST)
        PFD=ProfileForm(request.POST,request.FILES)
        if USFD.is_valid() and PFD.is_valid():
            NSUFO=USFD.save(commit=False)
            SUBPWD=USFD.cleaned_data['password']
            NSUFO.set_password(SUBPWD)
            NSUFO.save()

            NSPFO=PFD.save(commit=False)
            NSPFO.username=NSUFO
            NSPFO.save()

            send_mail('REGISTRATION DETAILS',
                    'Your Registration is Successful',
                    'sudheersaanika11@gmail.com',
                    [NSUFO.email],
                    fail_silently=False
                    
            )
            return HttpResponse('<center><h1>Registration is Completed Successfully...!</h1></center>')

    return render(request,'registration.html',d)



def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)

    return render(request,'home.html')



def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO:
            if AUO.is_active:
                login(request,AUO)
                request.session['username']=username
                return HttpResponseRedirect(reverse('home'))

            else:
                return HttpResponse('<center><h1>Not a Active User</h1></center>')

        else:
            return HttpResponse('<center><h1>Invalid Details</h1></center>')

    return render(request,'user_login.html')



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def display_details(request):
    username=request.session['username']
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}

    return render(request,'display_details.html',d)


@login_required
def change_password(request):
    if request.method=='POST':
        pw=request.POST['pw']
        username=request.session['username']
        UO=User.objects.get(username=username)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('<center><h1>Password is Changed Successfully</h1></center>')

    return render(request,'change_password.html')


def reset_password(request):
    if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']

        LUO=User.objects.filter(username=un)
        if LUO:
            UO=LUO[0]
            UO.set_password(pw)
            UO.save()
            return HttpResponse('<center><h1>Password Reset Successfully</h1></center>')
        else:
            return HttpResponse('<center><h1>Invalid Username</h1></center>')

    return render(request,'reset_password.html')