from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Todo


def home(request):
    tasks = None
    user_info = None

    if request.user.is_authenticated:
        user_info = {
            'username': request.user.username,
            'email': request.user.email
        }

        tasks = Todo.objects.filter(user=request.user)

    return render(request, "todo/home.html", {'user_info': user_info, 'tasks': tasks})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log in the user
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "todo/login.html", {})


def logout_view(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if len(password) < 6:
            messages.error(
                request, "The password needs to be at least 6 characters")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(
                request, "Username already exists. Use a unique one.")
            return redirect("register")

        user = User.objects.create_user(
            username=username, email=email, password=password)
        user.save()

        messages.success(
            request, "Registration successful. You can now log in.")

        return redirect('login')

    return render(request, "todo/register.html", {})


def createtask(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        category = request.POST['category']

        user = request.user

        todo = Todo.objects.create(
            title=title, description=description, category=category, user=user)
        todo.save()
        messages.success(request, "Task created successfully")

        return redirect('home')
    categories = Todo.CATEGORY_CHOICES
    return render(request, 'todo/createtask.html', {'categories': categories})
