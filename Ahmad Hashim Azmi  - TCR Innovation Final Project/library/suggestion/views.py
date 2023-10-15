from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SuggestionsForm

@login_required(login_url='login')
def suggestion_form_view(request):
    if request.method == 'POST':
        form = SuggestionsForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'suggestion/success_page.html')
    
    else:
        form = SuggestionsForm()

    return render(request, 'suggestion/suggest.html', {'form': form})

@login_required(login_url='login')
def success_page(request):
    return render(request, 'suggestion/success_page.html')