from django.shortcuts import render

# Create your views here.
def cart(request):

    cart = request.session.get('cart', {})

    cart_items = []

    total = 0

    for product_id, quantity in cart.items():

        product = get_object_or_404(Product, id=product_id)

        subtotal = product.price * quantity

        total += subtotal

        cart_items.append({

            'product': product,

            'quantity': quantity,

            'subtotal': subtotal

        })

    delivery_charge = 40 if total > 0 else 0

    grand_total = total + delivery_charge

    context = {

        'cart_items': cart_items,

        'total': total,

        'delivery_charge': delivery_charge,

        'grand_total': grand_total,

    }

    return render(request, 'cart.html', context)

    def increase_quantity(request, id):

    cart = request.session.get('cart', {})

    product_id = str(id)

    if product_id in cart:

        cart[product_id] += 1

    request.session['cart'] = cart

    return redirect('cart')

    def decrease_quantity(request, id):

    cart = request.session.get('cart', {})

    product_id = str(id)

    if product_id in cart:

        if cart[product_id] > 1:

            cart[product_id] -= 1

        else:

            del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')

    def remove_from_cart(request, id):

    cart = request.session.get('cart', {})

    product_id = str(id)

    if product_id in cart:

        del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')