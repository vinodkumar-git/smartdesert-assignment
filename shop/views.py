from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product, Category, Contact
from django.core.paginator import Paginator, InvalidPage, EmptyPage

# Create your views here.
def index(request):
    text_var = '<h3>Hello. Please Click the link to enter into the ecommerce site: </h3><h4><a href="http://127.0.0.1:8000/shop">Click here</a></h4><h3> OR <br/> <br/>You can search using this link: http://127.0.0.1:8000/shop <h3/>'
    return HttpResponse(text_var)

def contactus(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        cont = Contact(name=name, email=email, subject=subject, message=message)
        cont.save()
        return render(request, 'shop/contact.html', {'Success': 'Submitted Successfully! Thank you for contacting us..'})
    else:
        return render(request, 'shop/contact.html')

#category View
def allProdCat(request, c_slug=None):
    c_page = None
    products_list = None
    if c_slug != None:
        c_page = get_object_or_404(Category, slug=c_slug)   #To get the categorylist (modelname, get_catgory_by_slugfield)
        products_list = Product.objects.all().filter(category=c_page, available=True) #to get prodcuts based on category
    else:
        products_list = Product.objects.all().filter(available=True)
    '''Paginator code'''
    paginator = Paginator(products_list, 6)  # mention the product and the limit of the items to be displayed in a page
    try:
        page = int(request.GET.get('page','1')) #converted into integer in order to get page no. 1
    except:     #else
        page = 1
    try:
        products = paginator.page(page)     #to get the page using paginator method
    except (EmptyPage, InvalidPage):    #else exception
        products = paginator.page(paginator.num_pages)  #paginator.page is method and put the total no. of pages
    return render(request, 'shop/category.html', {'category':c_page, 'products':products})

#each product details.
def ProdCatDetail(request, c_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=c_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, 'shop/product.html', {'product': product})