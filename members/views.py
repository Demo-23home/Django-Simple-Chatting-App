from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from chat.models import Group


def user_signup(request):
    if request.method == "POST":
        data = request.POST

        email = data.get("email", "").strip()
        username = data.get("username", "").strip()
        passwd = data.get("password", "").strip()

        user_model = get_user_model()

        if not username:
            messages.error(request, "Username cannot be empty!")
            return render(request, "user/sign_up.html")

        if user_model.objects.filter(email=email).exists():
            messages.error(request, "Duplicated email!")
            return render(request, "user/sign_up.html")

        user = user_model.objects.create_user(email=email, password=passwd)
        user.username = username
        user.set_password(passwd)
        user.save()

        user_auth = authenticate(username=email, password=passwd)
        if user_auth:
            login(request, user_auth)
            return redirect("home")

        messages.error(request, "Authentication failed.")
        return render(request, "user/sign_up.html")

    return render(request, "user/sign_up.html")


def user_login(request):
    if request.method == "POST":
        data = request.POST

        email = data.get("email", "").strip()
        passwd = data.get("password", "").strip()

        user_auth = authenticate(username=email, password=passwd)

        if user_auth:
            login(request, user_auth)
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, "user/login.html")

    return render(request, "user/login.html")


def logout(request):  # noqa: F811
    try:
        logout(request)
    except:  # noqa: E722
        messages.error(request, "Something is wrong!")

    return redirect("login")


@login_required
def home(request):
    groups = Group.objects.all()
    context = {"groups": groups}
    return render(request, "user/home.html", context=context)
