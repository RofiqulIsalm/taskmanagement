from django.shortcuts import render, redirect, get_object_or_404
from application.EmailBackEnd import EmailBackEnd
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from application.models import Task,Photo
def base(request):
    return render(request, 'base.html')
def Login(request):
    return render(request, 'auth/login.html')
def dologin(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        user_password = request.POST.get('password')
        
        user = authenticate(request, username=user_name, password=user_password)
        
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect('desh_page')
            else:
                messages.error(request, 'Your account is not active.')
                return redirect('login_page')
        else:
            messages.error(request, 'User not valid...!')
            return redirect('login_page')
@login_required(login_url='/login/')        
def dologout(request):
    logout(request)
    return redirect('login_page')
def register(request):
    if request.method == 'POST':
        # print(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request,'User Already Exists...!')
            return redirect('register_page')
        else:
            user = User.objects.create_user(username, email, password)
            user.save()
            return redirect('login_page')
    return render(request, 'auth/registration.html')
def forgot(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Check if the email exists in the database
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Email not found in our records.')
        else:
            # Generate a password reset link and send it to the user's email
            # You would typically generate a unique token and create a password reset link.
            # For simplicity, we're just sending a placeholder message here.
            reset_link = "https://example.com/reset-password/"  # Replace with your actual reset link
            message = f"Click the following link to reset your password: {reset_link}"
            send_mail('Password Reset', message, 'your@example.com', [email])

            messages.success(request, 'Password reset link has been sent to your email.')

    return render(request, 'auth/forgot.html')

@login_required(login_url='/login/')
def desh(request):
    tasks = Task.objects.filter(user=request.user) 
    context = {
        'tasks': tasks,
    }
    return render(request, 'main/desh.html', context)
@login_required(login_url='/login/')
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        photo = request.FILES.get('photo')

        if title and description and due_date and priority and photo:
            new_task = Task(
                user=request.user,
                title=title,
                description=description,
                due_date=due_date,
                priority=priority,
            )
            new_task.save()

            new_photo = Photo(image=photo, task=new_task)
            new_photo.save()

            return redirect('desh_page')

    return render(request, 'main/desh.html')

def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        task.delete()
    except Task.DoesNotExist:
        pass  

    return redirect('task_list') 

def task_list(request):
    tasks = Task.objects.all() 
    return render(request, 'main/desh.html', {'tasks': tasks})

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')

        task.title = title
        task.description = description
        task.due_date = due_date
        task.priority = priority
        task.save() 
        return redirect('desh_page') 
    return render(request, 'main/desh.html', {'task': task})

def search_task(request):
    query = request.GET.get('q', '')

    tasks = Task.objects.filter(title__icontains=query)

    context = {
        'tasks': tasks,
        'query': query,
    }

    return render(request, 'main/desh.html', context)
@login_required(login_url='/')  
def profile(request):
        
    return render(request, 'auth/profile.html')

def password_change(request):
    if request.method == "POST":
        pwd = request.POST.get('cpwd')
        npwd = request.POST.get('npwd')
        
        try:
            custormuser = User.objects.get(id=request.user.id)
            cpwd = custormuser.check_password(pwd)
            if cpwd:
               custormuser.set_password(npwd)
               custormuser.save()
               messages.success(request, 'Password Change Successful...!')
            else:
               messages.error(request, 'Password Change faild...!')
        except User.DoesNotExist:
           messages.error(request, 'User not found...!')
        return redirect('profile_page')
    return render(request, 'auth/profile.html')