from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from .models import Books, Categories
from account.models import UserProfile, MyBooks
from django.contrib.auth.models import User
from django import forms
import random


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'home/signup.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        print("Form data: ", form.cleaned_data)
        response = super().form_valid(form)

        user = self.object
        UserProfile.objects.create(user = user)

        login(self.request, self.object)
        return response

class LogoutInterfaceView(LogoutView):
    template_name = "home/logout.html"

class LoginInterfaceView(LoginView):
    template_name = "home/login.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)


def home(request):
    categories = Categories.objects.all()

    books = Books.objects.all
    categories_with_books = []

    for category in categories:
        books_in_category = Books.objects.filter(category=category)
        if books_in_category:
            categories_with_books.append({
                'category': category,
                'books': books_in_category
            })

    if categories_with_books:
        random_category = random.choice(categories_with_books)
        carousel_books = random_category['books'][:8]
    else:
        random_category = None
        carousel_books = []

    return render(request, 'home/home.html', {'books':books , 'carousel_books':carousel_books, 'categories':categories, 'categories_with_books':categories_with_books})




def about(request):
    return render(request, 'home/about.html')




def browse(request, page_number = 1):
    query = request.GET.get('query')

    books = Books.objects.order_by('title')

    if query:
        books = books.filter(title__icontains=query)

    books_per_page = 12

    paginator = Paginator(books, books_per_page)

    try:
        current_page = paginator.page(page_number)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)

    return render(request, 'home/browse.html', {'current_page': current_page, 'query': query})



def book(request, book_id):
    book = get_object_or_404(Books, id = book_id)

    return render(request, 'home/book.html', {'book': book})


@login_required
def add_to_my_books(request, book_id):
    book = get_object_or_404(Books, id = book_id)
    user = request.user

    if not MyBooks.objects.filter(user = user, book = book).exists():
        MyBooks.objects.create(user = user, book = book)
        messages.success(request, f'Successfully added {book.title} to My Books.')
    else:
        messages.info(request, f'{book.title} is already in your My Books.')

    return redirect('book', book_id = book_id)