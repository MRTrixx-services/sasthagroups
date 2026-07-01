from django.shortcuts import render

def home(request):
    return render(request, "flowers/flowers.html")