from django.shortcuts import render

# Create your views here.

def index(request,channel):
    return render(request,'core/index.html',{"channel":channel})