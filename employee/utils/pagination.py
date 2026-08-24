from django.core.paginator import Paginator


def paginate_queryset(request, queryset, page_size: int = 10):
    """Paginate a queryset and return the page object."""
    paginator = Paginator(queryset, page_size)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)
