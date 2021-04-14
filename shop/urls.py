
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.allProdCat, name='allProdCat'), #display all products
    path('<slug:c_slug>/', views.allProdCat, name='products_by_category'),  #all products based on category slugs
    path('<slug:c_slug>/<slug:product_slug>/', views.ProdCatDetail, name='ProdCatDetail'),
]