from django import forms
from .models import Suggestions

class SuggestionsForm(forms.ModelForm):
    class Meta:
        model = Suggestions
        fields = ['title', 'author', 'year_released', 'description']