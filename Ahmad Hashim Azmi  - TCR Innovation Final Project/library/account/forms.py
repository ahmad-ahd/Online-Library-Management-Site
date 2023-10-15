from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from home.models import Books, Categories

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class PasswordChangeForm(PasswordChangeForm):
    pass

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class UserProfileImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']




class AddBookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['title', 'content', 'summary', 'author', 'category', 'thumbnail']

    content = forms.FileField(widget = forms.ClearableFileInput(attrs = {'accept': '.pdf'}), required = False)
    thumbnail = forms.ImageField(widget = forms.ClearableFileInput(attrs = {'accept': 'image/*'}), required = False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Categories.objects.all()


class EditBookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['title', 'author', 'summary', 'content', 'category', 'thumbnail']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Categories.objects.all()