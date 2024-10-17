from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Todo as todo
from django.contrib.auth.decorators import login_required



@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')  
        new_todo = todo(user=request.user, todo_name=task)
        new_todo.save()

    all_todos = todo.objects.filter(user=request.user)
    context = {
        'todos': all_todos
    }
    return render(request, 'todolist_app/todo.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')  
        if len(password) < 3:
            messages.error(request, 'Password must be at least 3 characters')
            return redirect('register')

        get_all_users_username = User.objects.filter(username=username)
        if get_all_users_username:
            messages.error(request, 'Error, user already exists. Use another username.')
            return redirect('register')

        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()

        messages.success(request, 'User successfully created. Log in now.')
        return redirect('login')
    return render(request, 'todolist_app/register.html', {})

def LogoutView(request):
    logout(request)
    return redirect('login')

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST': 
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home-page')
        else:
            messages.error(request, 'Error, wrong user details or user does not exist')
            return redirect('login')
    return render(request, 'todolist_app/login.html', {})


@login_required
def DeleteTask(request, id):
    todos_to_delete = todo.objects.get(id = id)
    todos_to_delete.delete()  
    return redirect('home-page')


@login_required
def Update(request, id):
    todos = todo.objects.get(id = id)
    todos.status = True
    todos.save() 
    return redirect('home-page')


