from django.conf.urls import url
from . import views 

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^register$', views.register, name="register"),
    url(r'^login$', views.login, name="login"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^quotes$', views.user, name="quotes"),
    url(r'^user/(?P<userId>\d+)$', views.userQuotes, name="userQuotes"),
    url(r'^myaccount/(?P<userId>\d+)$', views.edit, name="edit"),
    url(r'^addQuote$', views.addQuote, name="addQuote"),
    url(r'^likeQuote/(?P<quoteId>\d+)$', views.likeQuote, name="likeQuote"),
    url(r'^delQuote/(?P<quoteId>\d+)$', views.delQuote, name="delQuote"),
    url(r'^updateAccount/(?P<userId>\d+)$', views.updateAccount, name="updateAccount")
]