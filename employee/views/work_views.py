from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator

from employee.models import Work 
from employee.models import Piecework
from employee.forms import WorkForm, UpdateWorkForm
from employee.views.delete_attention import send_delete_warning


def create_work(request):
    """View to create a new work."""
    if request.method == 'POST':
        form = WorkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('work_list')
    else:
        form = WorkForm()

    return render(
        request,
        'work/create_work.html',
        {
            'form': form,
            'object_type': 'Work',
            'cancel_url': reverse('work_list'),
        }
    )


def work_list(request):
    """View to list all works with filtering and pagination."""
    works = Work.objects.all()

    # Filtering
    work_name = request.GET.get('work_name')
    department = request.GET.get('department')

    if department:
        works = works.filter(department__icontains=department)
    if work_name:
        works = works.filter(work_name__icontains=work_name)

    departments = Work.objects.values_list('department', flat=True).distinct()

    paginator = Paginator(works, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'work/work_list.html',
        {
            'works': page_obj,
            'page_obj': page_obj,
            'departments': departments,
        }
    )


def update_work(request, pk):
    """View to update an existing work."""
    work = get_object_or_404(Work, pk=pk)

    if request.method == 'POST':
        form = UpdateWorkForm(request.POST, instance=work)
        if form.is_valid():
            form.save()
            return redirect('work_list')
    else:
        form = UpdateWorkForm(instance=work)
        
    return render(
        request,
        'work/update_work.html',
        {
            'form': form,
            'object_type': 'Work',
            'object_name': work.work_name,
            'cancel_url': reverse('work_list'),
        }
    )


def delete_work(request, pk):
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
        object_name = work.work_name
        work.delete()
        send_delete_warning(request, object_name)
        return redirect('work_list')
