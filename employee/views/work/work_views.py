from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator

from employee.models import Work 
from employee.models import Piecework
from employee.forms import WorkForm, UpdateWorkForm
from employee.utils.delete_attention import send_delete_warning


def work_create(request):
    """View to create a new work."""
    department = request.GET.get('department') or request.session.get('department')

    if request.method == 'POST':
        form = WorkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('work_list')
    else:
        form = WorkForm()

    return render(
        request,
        'work/work_create.html',
        {
            'form': form,
            'object_type': 'Work',
            'selected_department': department,
            'cancel_url': reverse('work_list'),
        }
    )


def work_list(request):
    """View to list all works with filtering and pagination."""
    works = Work.objects.all()

    # Filtering
    department = request.GET.get('department') or request.session.get('department')
    work_name = request.GET.get('work_name')

    if department:
        works = works.filter(department__icontains=department)
    if work_name:
        works = works.filter(work_name__icontains=work_name)

    # Ensure consistent ordering for pagination
    works = works.order_by('work_name')

    paginator = Paginator(works, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'work/work_list.html',
        {
            'works': page_obj,
            'page_obj': page_obj,
            'selected_department': department,
        }
    )


def work_update(request, pk):
    """View to update an existing work."""
    work = get_object_or_404(Work, pk=pk)
    department = request.GET.get('department') or request.session.get('department')

    if request.method == 'POST':
        form = UpdateWorkForm(request.POST, instance=work)
        if form.is_valid():
            form.save()
            return redirect('work_list')
    else:
        form = UpdateWorkForm(instance=work)
        
    return render(
        request,
        'work/work_update.html',
        {
            'form': form,
            'object_type': 'Work',
            'object_name': f"{work.work_name}",
            'selected_department': department,
            'cancel_url': reverse('work_list'),
        }
    )


def work_delete(request, pk):
    """View to delete an existing work."""
    work = get_object_or_404(Work, pk=pk)
    related_pieceworks = Piecework.objects.filter(work=work)
    if related_pieceworks.exists():
        messages.error(
            request,
            f"Cannot delete <b>{work.work_name}</b> because it is associated with piecework records."
        )
        return redirect('work_list')
    if request.method == 'POST':
        object_name = f"{work.work_name}"
        work.delete()
        send_delete_warning(request, object_name)

        return redirect('work_list')
