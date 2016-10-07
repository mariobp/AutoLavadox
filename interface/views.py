from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return render(request, 'home/index.html')
# end def


def login(request):
    return render(request, 'home/login.html')
# end def


def addvehiculo(request):
    return render(request, 'home/addvehiculo.html')
# end def
