from django.contrib import admin

# Register your models here.
from .models import Category, Product, Contact

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','stock', 'available','created', 'updated']   #attributes that are to be displayed.
    list_editable = ['price','stock','available']   #that can be editable without actually accessing the fields
    prepopulated_fields = {'slug':('name',)}
    list_per_page = 20  #show only 20 products per page
admin.site.register(Product, ProductAdmin)

admin.site.register(Contact)