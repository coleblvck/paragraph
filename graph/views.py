from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from account.models import Account
from django.views.decorators.cache import never_cache

# Create your views here.

@never_cache
def index(request):
    context = {}
            
    return render(request, "graph/index.html", context)

