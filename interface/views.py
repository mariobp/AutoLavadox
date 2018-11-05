from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='/empleados/login/')
def index(request):
    return render(request, 'home/index.html')
# end def


def addvehiculo(request):
    return render(request, 'home/addvehiculo.html')
# end def
