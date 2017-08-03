from django.shortcuts import render
from MainAPP.models import Videos

# Create your views here.
def index(request):

    return render(request, 'MainAPP/index.html',context={})
def article(request):
    pass