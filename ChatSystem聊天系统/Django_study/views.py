import os
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, reverse, redirect
def home(request):
    return render(request,'../static/index.html')


def home2(request):
    return render(request,'../static/main.html')