from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def home(request):
    return render(request,'score_cards/index.html')



def about(request):
    return render(request,'score_cards/about.html')


def role(request):
    return render(request,'score_cards/roles.html')