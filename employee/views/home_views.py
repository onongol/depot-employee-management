from django.shortcuts import render


def home(request):
    """View to render the home page."""
    return render(request, 'home.html')
