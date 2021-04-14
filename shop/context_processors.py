# to browse via categories and categry links available across website
from .models import Category

def menu_links(request):
    links = Category.objects.all()
    return dict(links = links)