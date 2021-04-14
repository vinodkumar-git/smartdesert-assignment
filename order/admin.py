from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.
class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    fieldsets = [
        ('Product', {'fields': ['product'],}),
        ('Quantity', {'fields': ['quantity'],}),
        ('Price', {'fields': ['price'],}),
    ]
    readonly_fields = ['product','quantity','price']
    #to remove the delete option
    can_delete = False
    max_num = 0 #tp avoid multiple lines in the order adminpanel
    template = 'admin/order/tabular.html'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','billingName','emailAddress','created']
    list_display_links = ('id','billingName')
    search_fields = ['id','billingName','emailAddress']
    #give readonly permission
    readonly_fields = ['id','total','emailAddress','created','billingName','billingAddress1','billingCity',
                       'billingPostcode','billingCountry','shippingName','shippingAddress1','shippingCity','shippingPostcode',
                       'shippingCountry']
    #To mention the order of the fields
    fieldsets = [
        ('ORDER INFORMATION',{'fields': ['id','total','created','status']}),
        ('BILLING INFORMATION', {'fields': ['billingName','billingAddress1','billingCity','billingPostcode','billingCountry','emailAddress']}),
        ('SHIPPING INFORMATION',{'fields': ['shippingName','shippingAddress1','shippingCity','shippingPostcode','shippingCountry']}),
    ]
    inlines = [
        OrderItemAdmin,     #inorder to see OrderItems as part of OrderAdmin
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
