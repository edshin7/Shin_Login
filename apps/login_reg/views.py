from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Author, Quote
import bcrypt

# Create your views here.
def index(request):
    if "curUserId" in request.session.keys():
        return redirect("/login_reg/quotes")
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

    messages.success(request, "Registration succsessful", extra_tags="success")
    return redirect("/login_reg/quotes")

def login(request):
    if(request.method != "POST"):
        return redirect("/login_reg")

    user = User.objects.filter(email=request.POST["email"])
    
    if len(user) == 1 and bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
        request.session["curUserId"] = user[0].id
        return redirect("/login_reg/quotes")

    messages.error(request, "Incorrect Email or Password", extra_tags="login")
    return redirect("/login_reg")

def user(request):
    if "curUserId" not in request.session.keys():
        return redirect("/login_reg")

    user = User.objects.get(id=request.session["curUserId"])
    context = {
        "user": user,
        "quotes": Quote.objects.all(),
        "curUserId": request.session["curUserId"]
    }
    return render(request, "user.html", context)

def logout(request):
    request.session.clear()
    return redirect("/login_reg")

def userQuotes(request, userId):
    if "curUserId" not in request.session.keys():
        return redirect("/login_reg")

    context = {
        "user": User.objects.get(id=userId)
    }

    return render(request, "userQuotes.html", context)

def edit(request, userId):
    if "curUserId" not in request.session.keys():
        return redirect("/login_reg")

    if int(userId) != request.session["curUserId"]:
        return redirect("/login_reg/logout")

    return render(request, "edit.html", { "user": User.objects.get(id=userId) })

def likeQuote(request, quoteId):
    if request.method != "POST":
        if "curUserId" not in request.session.keys():
            return redirect("/login_reg")
        return redirect("/login_reg/quotes")

    user = User.objects.get(id=request.session["curUserId"])
    if len(user.liked_quotes.filter(id=quoteId)) == 0:
        quote = Quote.objects.get(id=quoteId)
        quote.likes.add(user)
    else:
        messages.error(request, "Already Liked", extra_tags="like")

    return redirect("/login_reg/quotes")

def delQuote(request, quoteId):
    if "curUserId" not in request.session.keys():
        return redirect("/login_reg")

    # check if quote exists
    if len(Quote.objects.filter(id=quoteId)) == 0:
        if "curUserId" not in request.session.keys():
            return redirect("/login_reg")
        return redirect("/login_reg/quotes")

    quote = Quote.objects.get(id=quoteId)

    # check if quote belongs to curUser
    if quote.uploader.id != request.session["curUserId"]:
        return redirect("/login_reg/logout")

    quote.delete()
    return redirect("/login_reg/quotes")

def addQuote(request):
    if request.method != "POST":
        if "curUserId" not in request.session.keys():
            return redirect("/login_reg")
        return redirect("/login_reg/quotes")

    authorErrors = Author.objects.validator(request.POST)
    quoteErrors = Quote.objects.validator(request.POST)
    hasErrors = False

    if len(authorErrors) > 0:
        for tag, error in authorErrors.items():
            messages.error(request, error, extra_tags=tag)
        hasErrors = True

    if len(quoteErrors) > 0:
        for tag, error in quoteErrors.items():
            messages.error(request, error, extra_tags=tag)
        hasErrors = True

    if hasErrors:
        return redirect("/login_reg/quotes")

    author = None
    if len(Author.objects.filter(name=request.POST["name"])) > 0:
        author = Author.objects.filter(name=request.POST["name"])[0]
    else:
        author = Author.objects.create(name=request.POST["name"])

    newQuote = Quote.objects.create(
        content = request.POST["content"],
        author = author,
        uploader = User.objects.get(id=request.session["curUserId"])
    )

    return redirect("/login_reg/quotes")

def updateAccount(request, userId):
    if request.method != "POST":
        if "curUserId" not in request.session.keys():
            return redirect("/login_reg")
        return redirect("/login_reg/quotes")

    if int(userId) != request.session["curUserId"]:
        return redirect("/login_reg/logout")

    errors = User.objects.validator_edit(request.POST)

    if len(errors) > 0:
        for tag, error in errors.items():
            messages.error(request, error, tag)
        return redirect("/login_reg/myaccount/" + str(userId))

    user = User.objects.get(id=request.session["curUserId"])
    user.first_name = request.POST["first_name"]
    user.last_name = request.POST["last_name"]
    user.email = request.POST["email"]
    user.save()

    messages.success(request, "Account successfully updated", extra_tags="success")
    return redirect("/login_reg/quotes")