from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
from empleados.decorators import is_user_redirect_view


@login_required(login_url='/empleados/login/')
@is_user_redirect_view
def index(request):
    return render(request, 'home/index.html')
# end def


def addvehiculo(request):
    return render(request, 'home/addvehiculo.html')
# end def
