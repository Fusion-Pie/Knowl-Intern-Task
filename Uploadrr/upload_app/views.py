from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from .models import Files
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

                return render(request, 'basePage.html')
            
            else:
                messages.error(request, 'Incorrect Username or Password')

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

                    user = authenticate(request, 
                        username = request.POST['uname'],
                        password = request.POST['pass'])
            
                    if user is not None:
                        login(request , user = user)

                    messages.success(request, "User Created Successfully")
                    
                    return render(request, 'basePage.html')
                except:
                    messages.error(request, "Something went wrong!! Please try again Later!!")
    
    return render(request, 'registerLoginPage.html')


@login_required(login_url = '/')
def base(request):
    return render(request, 'basePage.html')


@login_required(login_url = '/')
def profile(request):
    userInfo = User.objects.get(username = request.user)
    return render(request, 'profilePage.html', context = {'user': userInfo})


@login_required(login_url = '/')
def uploadFile(request):
    # Save the uploaded files in the db
    if request.method == 'POST':
        if request.POST['btn_name'] == 'Upload':
            for file in request.FILES.getlist('files'):
                new_file = Files.objects.create(file_name = file.name, 
                                                file = file,
                                                uploadedBy = request.user)

                new_file.save()

    return render(request, 'uploadPage.html')


@login_required(login_url = '/')
def viewUploadedFiles(request):
    files = list(Files.objects.filter(uploadedBy = request.user).values())

    if request.method == 'POST':
        if request.POST['btn_name'] == 'Share':
            try:
                file = Files.objects.get(id = request.POST['fid'])
                user = User.objects.get(username = request.POST['uname'])

                file.shared_with.add(user)
                file.save()
            except:
                pass

    return render(request, 'uploadedFiles.html', context = {'files': files})


@login_required(login_url = '/')
def searchUser(request):
    context = {}
 
    if request.method =='POST':
        if request.POST['btn_name'] == 'Find':
            try:
                user = User.objects.filter(username = request.POST['uname'])
                context['userInfo'] = user 
            except:
                pass

    return render(request, 'searchUserPage.html', context = context)

@login_required(login_url = '/')
def sharedFiles(request):
    user = User.objects.get(username = request.user)

    files = user.shared_with.all()

    return render(request, 'sharedFilePage.html', context = {'files': files})


def logoutUser(request):
    logout(request)
    return redirect('/')