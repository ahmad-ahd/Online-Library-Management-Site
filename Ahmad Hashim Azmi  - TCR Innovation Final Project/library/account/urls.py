from django.urls import path
import account.views
from .views import update_profile_picture

urlpatterns = [
    path('account', account.views.account, name = "account"),
    path('update_profile_picture', update_profile_picture, name='update_profile_picture'),
    path('manage_books', account.views.manage_books, name = "manage_books"),
    path('add_book', account.views.add_book, name = "add_book"),
    path('edit_book/<int:book_id>', account.views.edit_book, name = "edit_book"),
    path('delete_book/<int:book_id>', account.views.delete_book, name = "delete_book"),
    path('create_category', account.views.create_category, name = "create_category"),
    path('delete_category/<int:category_id>', account.views.delete_category, name = "delete_category"),
    path('edit_category/', account.views.edit_category, name='edit_category'),
    path('my_books', account.views.my_books, name = "my_books"),
    path('remove_book_from_list/<int:my_book_id>', account.views.remove_book_from_list, name = "remove_book_from_list"),
    path('update_profile_picture', account.views.update_profile_picture, name = "update_profile_picture"),
]