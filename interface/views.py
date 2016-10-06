from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'home/index.html')
# end def


def login(request):
    return render(request, 'home/login.html')
# end def
