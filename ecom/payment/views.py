from django.shortcuts import render
from django.http import JsonResponse

from .models import ShippingAddress, Order, OrderItem
from cart.cart import Cart

def checkout(request):
    if request.user.is_authenticated:
        try:
            # check if user has a shipping address
            shipping_address = ShippingAddress.objects.get(user=request.user.id)

            context = {"shipping": shipping_address}

            return render(request, "payment/checkout.html", context=context)

        except:
            # if user does not have a shipping address
            return render(request, "payment/checkout.html")

    else:
        # Guest user
        return render(request, "payment/checkout.html")
    
    
def complete_order(request):
    
    if request.POST.get('action') == 'post':
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        
        # All-in-one shipping address
        shipping_address = (address1 + "\n" + address2 + "\n" + city + "\n" + state + "\n" + zipcode)
        
        # Shopping cart information
        
        cart = Cart(request)
        
        total_cost = cart.get_total()
        
        if request.user.is_authenticated:
            # Create an order for authenticated user
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=total_cost,
                user=request.user
            )
            
            order_id = order.pk

            for item in cart:
                
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item['product'],
                    quantity=item['qty'],
                    price=item['price'],
                    user=request.user
                )
        # Create an order for guest user 
        else:        
        
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=total_cost
            )
                
            order_id = order.pk

            for item in cart:
                    
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item['product'],
                    quantity=item['qty'],
                    price=item['price']
                )
        
        order_success = True
        
        return JsonResponse({'success': order_success})   
       
    return render(request, "payment/complete-order.html")


def payment_success(request):
    
    # clear the cart
    for key in list(request.session.keys()):
        
        if key == 'session_key':
            
            del request.session[key]
     
    return render(request, "payment/payment-success.html")


def payment_failed(request):
    return render(request, "payment/payment-failed.html")