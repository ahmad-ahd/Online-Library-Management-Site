from django.urls import path
import suggestion.views
from . import views

urlpatterns = [
    path('suggest', suggestion.views.suggestion_form_view, name = "suggest"),
    path('success_page', suggestion.views.success_page, name = "success_page"),
]