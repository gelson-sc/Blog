import datetime
from apps.blog.models import Category


def get_site_context(request):
    current_datetime = datetime.datetime.now()
    categories = Category.objects.filter(active=True)

    return {
        'current_year': current_datetime.year,
        'categories': categories,
    }


