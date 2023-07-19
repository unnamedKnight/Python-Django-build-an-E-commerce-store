from django.shortcuts import render

# Create your views here.a

def register(request):
    return render(request, 'account/register.html')
