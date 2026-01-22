from django.core.paginator import Paginator


def paginate_queryset(request, queryset, page_size=10):
    """Paginate a queryset and return the page object."""
    paginator = Paginator(queryset, page_size)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj
