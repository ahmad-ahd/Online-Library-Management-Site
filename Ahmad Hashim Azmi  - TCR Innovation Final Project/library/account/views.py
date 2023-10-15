from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import UserUpdateForm, PasswordChangeForm, UserProfileImageForm, AddBookForm, EditBookForm
from home.models import Books, Categories
from account.models import MyBooks
from django.contrib import messages
from django.http import Http404
import os

@login_required
def account(request):
    user = request.user
    user_form = UserUpdateForm(instance=user)
    password_form = PasswordChangeForm(user)

    if request.method == 'POST':
        if 'update_user_info' in request.POST:
            user_form = UserUpdateForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "Successfully updated user info!")
                return redirect('account')

        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, "Successfully changed the password!")
                return redirect('account')

    return render(request, 'account/account.html', {'user_form': user_form, 'password_form': password_form})

@login_required
def update_profile_picture(request):
    old_profile_picture = request.user.userprofile.profile_picture
    old_profile_picture_name = request.user.userprofile.profile_picture.name

    if request.method == 'POST':
        form = UserProfileImageForm(request.POST, request.FILES, instance = request.user.userprofile)
        
        if form.is_valid():
            user_profile = form.save(commit = False)
            user_profile.save()

            if old_profile_picture and old_profile_picture_name != 'images/profile_pictures/default_pfp.png':
                if os.path.isfile(old_profile_picture.path):
                    os.remove(old_profile_picture.path)

            messages.success(request, "Successfully changed the profile picture!")
            return redirect('account')
    else:
        form = UserProfileImageForm(instance = request.user.userprofile)
    return render(request, 'profile_picture_form.html', {'form': form})






def my_books(request):
    query = request.GET.get('query')
    user = request.user

    my_books = MyBooks.objects.filter(user = user).select_related('book').order_by('book__title')

    if query:
        my_books = my_books.filter(book__title__icontains = query)


    return render(request, 'account/my_books.html', {'my_books': my_books})

def remove_book_from_list(request, my_book_id):
    my_book = get_object_or_404(MyBooks, pk = my_book_id)

    if my_book.user != request.user:
        raise Http404("Unauthorized Access!")
    
    messages.info(request, f"Successfully removed {my_book.book.title} from your list!")
    my_book.delete()
    return redirect('my_books')






def add_book(request):
    categories = Categories.objects.all()

    if request.method == 'POST':
        add_form = AddBookForm(request.POST, request.FILES)
        if add_form.is_valid():
            add_form.save()
            messages.success(request, "Book successfully added!")
            return redirect('manage_books')

    else:
        add_form = AddBookForm()

    return render(request, 'account/add_book.html', {'categories': categories})


def manage_books(request):
    categories = Categories.objects.all()
    query = request.GET.get('query')
    
    books = Books.objects.order_by('title')

    if query:
        books = books.filter(title__icontains=query)

    return render(request, 'account/manage_books.html', {'books': books, 'query': query, 'categories': categories})



def edit_book(request, book_id):
    categories = Categories.objects.all()
    book = get_object_or_404(Books, id = book_id)


    if request.method == 'POST':
        edit_form = EditBookForm(request.POST, request.FILES, instance = book)
        old_content = book.content
        old_thumbnail = book.thumbnail

        if edit_form.is_valid():
            if 'content' in request.FILES:
                new_content = request.FILES['content']
                if book.content:
                    os.remove(old_content.path)
                book.content = new_content


            if 'thumbnail' in request.FILES:
                new_thumbnail = request.FILES['thumbnail']
                if book.thumbnail:
                    os.remove(old_thumbnail.path)
                book.thumbnail = new_thumbnail


            book.save()
            messages.success(request, "Successfully saved changes to " + book.title + "!")
            return redirect('manage_books')

    else:
        edit_form = EditBookForm(instance = book)


    return render(request, 'account/edit_book.html', {'book': book, 'edit_form': edit_form, 'categories': categories})



def delete_book(request, book_id):
    book = get_object_or_404(Books, id = book_id)

    DEFAULT_CONTENT_PATH = 'books/Coming_Soon_Page.jpg'
    DEFAULT_THUMBNAIL_PATH = 'images/book_cover_not_available.jpg'

    is_default_content = book.content.path == DEFAULT_CONTENT_PATH
    is_default_thumbnail = book.thumbnail.path == DEFAULT_THUMBNAIL_PATH

    if request.method == 'POST':
        book.delete()
        if (is_default_content):
            os.remove(book.content.path)
        if (is_default_thumbnail):
            os.remove(book.thumbnail.path)
        messages.success(request, f"Successfully removed {book.title} from the database!")
        return redirect('manage_books')

    return render(request, 'account/delete_book.html', {'book': book})



def create_category(request):
    categories = Categories.objects.all()

    if request.method == 'POST':

        name = request.POST['name']
        Categories.objects.create(name = name)

        messages.success(request, f"Successfully added new category: {name}")
        return redirect('create_category')
    return render(request, 'account/create_category.html', {'categories': categories})

def delete_category(request, category_id):
    category = get_object_or_404(Categories, id=category_id)

    category.delete()
    messages.success(request, f"Successfully deleted category: {category.name}")
    return redirect('create_category')

def edit_category(request):
    if request.method == 'POST':
        category_id = request.POST.get('id')
        new_name = request.POST.get('name')

        try:
            category = Categories.objects.get(id = category_id)
            category.name = new_name
            category.save()
            messages.success(request, f'Successfully edited category: {category.name}')
        except Categories.DoesNotExist:
            messages.error(request, 'Category not found.')

    return redirect('create_category')