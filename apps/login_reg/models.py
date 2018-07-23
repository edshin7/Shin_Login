from django.db import models
from datetime import datetime, date
import re

# Create your models here.
class UserManager(models.Manager):
    def validator_reg(self, postData):
        errors = {}
        today = date.today()
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData["first_name"]) < 2:
            errors["first_name"] = "First name must have 2+ letters"
        elif not postData["first_name"].isalpha():
            errors["first_name"] = "Letters only for first name"

        if len(postData["last_name"]) < 2:
            errors["last_name"] = "Last name must have 2+ letters"
        elif not postData["last_name"].isalpha():
            errors["last_name"] = "Letters only for last name"

        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid Email"

        if len(postData["password"]) < 8:
            errors["password"] = "Password must have 8+ characters"
        elif postData["password"] != postData["confirm"]:
            errors["password"] = "Password must match confirmation"

        print(postData["birthday"])
        if len(postData["birthday"]) < 10:
            errors["birthday"] = "Birthday cannot be blank"
        elif datetime.strptime(postData["birthday"], '%Y-%m-%d') >= datetime.today():
            errors["birthday"] = "Birthday should be before today"

        return errors

    def validator_edit(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData["first_name"]) < 2:
            errors["first_name"] = "First name must have 2+ letters"
        elif not postData["first_name"].isalpha():
            errors["first_name"] = "Letters only for first name"

        if len(postData["last_name"]) < 2:
            errors["last_name"] = "Last name must have 2+ letters"
        elif not postData["last_name"].isalpha():
            errors["last_name"] = "Letters only for last name"

        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid Email"
        elif postData["originalEmail"] != postData["email"] and len(User.objects.filter(email=postData["email"])) == 1:
            errors["email"] = "Email already used"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    birthday = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class AuthorManager(models.Manager):
    def validator(self, postData):
        errors = {}

        checkName = postData["name"].replace(" ", "")
        if len(checkName) < 3:
            errors["name"] = "Name must have 3+ letters"
        elif not checkName.isalpha():
            errors["name"] = "Letters only"

        return errors

class Author(models.Model):
    name = models.CharField(max_length=255)

    objects = AuthorManager()


class QuoteManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData["content"].replace(" ", "")) < 10:
            errors["content"] = "Quote must have 10+ characters"

        return errors

class Quote(models.Model):
    content = models.TextField()
    author = models.ForeignKey(Author, related_name="quotes")
    uploader = models.ForeignKey(User, related_name="quotes")
    likes = models.ManyToManyField(User, related_name="liked_quotes")

    objects = QuoteManager()