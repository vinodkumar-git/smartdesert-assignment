from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from order.models import Order, OrderItem

# Create your views here.
#check if session id has been created or not
def _cart_id(request):
    cart = request.session.session_key
    if not cart:    #if there is NO session or if cart doesn't exists
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # get the cart by id
    except Cart.DoesNotExist:
        cart = Cart.objects.create(  # we will create a cart if cart doesnt exsits
            cart_id=_cart_id(request)
        )
        cart.save()
    try:  # we will try to add the cart item
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:  # if cartitem doesnt exists
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()
    return redirect('cart:cart_detail')

#show the items in the shopping cart
def cart_detail(request, price=0, total = 0, tax = 0, counter=0, cart_items = None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  #session
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            price += (cart_item.product.price * cart_item.quantity)
            tax = (price * 4) / 100
            total = price + tax
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html', dict(cart_items=cart_items, total=total, tax=tax, counter=counter))

def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')

def full_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')


def address_details(request, total=0, counter=0, cart_items = None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  #session
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    description = 'Smart Dessert Courses - New Order'

    if request.method == 'POST':
        # print(request.POST)
        try:
            billingName = request.POST['billingName']
            billingEmail = request.POST['billingEmail']
            billingAddress1 = request.POST['billingAddress1']
            billingCity = request.POST['billingCity']
            billingPostcode = request.POST['billingPostcode']
            billingCountry = request.POST['billingCountry']
            shippingName = request.POST['shippingName']
            shippingEmail = request.POST['shippingEmail']
            shippingAddress1 = request.POST['shippingAddress1']
            shippingCity = request.POST['shippingCity']
            shippingPostcode = request.POST['shippingPostcode']
            shippingCountry = request.POST['shippingCountry']

            try:
                order_details = Order.objects.create(
                    total = total,
                    emailAddress = billingEmail,
                    billingName = billingName,
                    billingAddress1 = billingAddress1,
                    billingCity = billingCity,
                    billingPostcode = billingPostcode,
                    billingCountry = billingCountry,
                    shippingName =shippingName,
                    shippingAddress1 = shippingAddress1,
                    shippingCity = shippingCity,
                    shippingPostcode = shippingPostcode,
                    shippingCountry = shippingCountry
                )
                order_details.save()
                print(order_details)
                #to create ordered item record that are in the cart.
                for order_item in cart_items:
                    oi = OrderItem.objects.create(
                        product = order_item.product.name,
                        quantity = order_item.quantity,
                        price = order_item.product.price,
                        order = order_details
                    )
                    oi.save()
                    #Reduce the stocks when the order is placed or saved
                    products = Product.objects.get(id=order_item.product.id)
                    products.stock = int(order_item.product.stock - order_item.quantity)
                    products.save()
                    order_item.delete()
                    #print this message when order is saved
                    print('The order is been created')
                    id = order_details.id
                    print(id)
                return redirect('order:thanks', order_details.id)
            except ObjectDoesNotExist:
                pass
        except ObjectDoesNotExist:
            pass
    return render(request, 'address.html',
                  dict(cart_items=cart_items, total=total, counter=counter, email=Order.emailAddress, name=Order.billingName,
                       description=description))
