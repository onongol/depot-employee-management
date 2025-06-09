from django.shortcuts import render


def home(request):
    """View to render the home page."""
    department = request.GET.get('department') or request.session.get('department')

    return render(
        request, 
        'home/home.html',
        {
            'selected_department': department
        }
    )
