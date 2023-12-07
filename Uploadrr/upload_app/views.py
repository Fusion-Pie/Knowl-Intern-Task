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
    if request.method == 'POST':
        if request.POST['btn_name'] == 'Logout':
            logout(request)
            messages.success(request, 'Logged Out Successfully!!')
        
            return redirect('/')
    

        # Save the uploaded files in the db
        if request.POST['btn_name'] == 'Upload':
            print(request.FILES.getlist('files'))
            
            for file in request.FILES.getlist('files'):
                new_file = Files.objects.create(file_name = file.name, 
                                                file = file,
                                                uploadedBy = request.user)
                
                user = User.objects.get(username = 'll')

                print(user)

                new_file.shared_with.add(user)

                new_file.save()

                print(user.shared_with.all())

            for file in  Files.objects.all():
                print(file.file_name, file.shared_with)

            messages.success(request, 'Files uploaded successfully')

            return HttpResponse("T")

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

    return render(request, 'uploadedFiles.html', context = {'files': files})


@login_required(login_url = '/')
def searchUser(request):
    context = {}
 
    if request.method =='POST':
        if request.POST['btn_name'] == 'Find':
            try:
                user = User.objects.filter(username = request.POST['uname'])
                context['userInfo'] = user 
                print(user)
            except:
                pass

    return render(request, 'searchUserPage.html', context = context)

def logoutUser(request):
    logout(request)
    return redirect('/')

def l(request):
    user = User.objects.get(username = 'Pie2')
    return HttpResponse(user.shared_with.all())