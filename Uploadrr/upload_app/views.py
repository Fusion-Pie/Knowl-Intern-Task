from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("All things are done in great way")