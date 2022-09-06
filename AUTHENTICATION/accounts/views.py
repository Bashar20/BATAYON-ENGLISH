from django.shortcuts import render
from accounts.models import Profile

# Create your views here.

def index(request):
    return render(request,'index.html')


def register(request):
    return render(request,'register.html')

def userLogin(request):
    return render(request,'login.html')
