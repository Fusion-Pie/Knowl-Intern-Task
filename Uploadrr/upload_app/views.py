from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def loginUser(request):
    if request.method == 'POST':
        if request.POST['btn_name'] == 'Login':
            user = authenticate(request, 
                                username = request.POST['uname'],
                                password = request.POST['pass'])
            
            if user is not None:
                login(request , user = user)

                messages.success(request, 'Login Successful !!')

                return render(request, 'basePage.html')
            
            else:
                messages.error(request, 'Username or Password is incorrect')

                return render(request, 'loginPage.html')

    return render(request, 'loginPage.html')


def registerUser(request):
    if request.method == 'POST':
        if request.POST['btn_name'] == 'Register':

            username_list = list( User.objects.values_list('username', flat = True) )
            
            if request.POST['uname'] in username_list:
                messages.error(request, "Please change the username")

                return render(request, 'registerLoginPage.html')
            
            else:
                new_user = User.objects.create_user(username = request.POST['uname'], 
                                password = request.POST['pass'],
                                first_name = request.POST['fname'],
                                last_name = request.POST['lname'])

                try:               
                    new_user.save()
                    messages.success(request, "User Created Successfully")
                    
                    return render(request, 'basePage.html')
                except:
                    messages.error(request, "Something went wrong!! Please try again Later!!")
                
            return HttpResponse("YEl")
    
    return render(request, 'registerLoginPage.html')


@login_required(login_url='/')
def base(request):
    if request.method == 'POST':
        if request.POST['btn_name'] == 'Logout':
            logout(request)
            messages.success(request, 'Logged Out Successfully!!')
        
        return redirect('/')

    return render(request, 'basePage.html')