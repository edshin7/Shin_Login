from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
import bcrypt

# Create your views here.
def index(request):
    if "curUserId" in request.session.keys():
        return redirect("/login_reg/welcome")
    return render(request, "index.html", {})

def register(request):
    if(request.method != "POST"):
        return redirect("/login_reg")

    errors = User.objects.validator_reg(request.POST)

    checkUser = User.objects.filter(
        email=request.POST["email"]
    )

    if len(checkUser) == 1 and not("email" in errors):
        errors["email"] = "Email already used"

    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val, extra_tags=key)

        return redirect("/login_reg")

    user = User.objects.create(
        first_name=request.POST["first_name"],
        last_name=request.POST["last_name"],
        email=request.POST["email"],
        birthday=request.POST["birthday"],
        password=bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
    )

    request.session["curUserId"] = user.id

    messages.success(request, "Registration succsessful")
    return redirect("/login_reg/welcome")

def login(request):
    if(request.method != "POST"):
        return redirect("/login_reg")

    user = User.objects.filter(email=request.POST["email"])
    
    if len(user) == 1 and bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
        request.session["curUserId"] = user[0].id
        return redirect("/login_reg/welcome")

    messages.error(request, "Incorrect Email or Password", extra_tags="login")
    return redirect("/login_reg")

def user(request):
    if "curUserId" not in request.session.keys():
        return redirect("/login_reg")

    user = User.objects.get(id=request.session["curUserId"])
    return render(request, "user.html", { "name": user.first_name })

def logout(request):
    request.session.clear()
    return redirect("/login_reg")