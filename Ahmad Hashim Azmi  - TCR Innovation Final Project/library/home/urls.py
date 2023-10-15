from django.urls import path
import home.views
from . import views

urlpatterns = [
    path('', home.views.home, name = "home"),
    path('login', views.LoginInterfaceView.as_view(), name = "login"),
    path('logout', views.LogoutInterfaceView.as_view(), name = "logout"),
    path('signup', views.SignupView.as_view(), name = "signup"),
    path('about', home.views.about, name = "about"),
    path('browse', home.views.browse, name = "browse"),
    path('browse/<int:page_number>', home.views.browse, name = "browse_paginated"),
    path('book/<int:book_id>', home.views.book, name = "book"),
    path('add_to_my_books/<int:book_id>', home.views.add_to_my_books, name = "add_to_my_books"),
]