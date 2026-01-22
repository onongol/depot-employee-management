from django.shortcuts import render


def home(request):    
    department = request.GET.get("department") or request.session.get("department")

    return render(request, "home/home.html", {"selected_department": department})
