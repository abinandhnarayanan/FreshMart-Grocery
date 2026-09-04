from decimal import Decimal
import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from .models import (
    Product,
    Category,
    UserProfile,
    Address,
    Order,
    OrderItem,
)

def index(request):
    return render(request, "index.html")


def fruits(request):
    return render(request, "fruits.html")


def vegetables(request):
    return render(request, "vegetables.html")

def dairy(request):
    products = Product.objects.filter(
        category__name="Dairy",
        available=True
    )

    return render(request, "dairy.html", {
        "products": products
    })


    

def grocery(request):
    products = Product.objects.filter(category__name="Grocery", available=True)

    return render(request, "grocery.html", {
        "products": products
    })


# PRODUCT DETAILS
def product_details(request, id):

    product = get_object_or_404(Product, id=id)

    return render(
        request,
        'product_details.html',
        {
            'product': product
        }
    )





# ADD TO CART
def add_to_cart(request, id):

    cart = request.session.get('cart', {})

    id = str(id)

    if id in cart:

        cart[id] += 1

    else:

        cart[id] = 1


    request.session['cart'] = cart

    request.session.modified = True

    return redirect('cart')


# CART
def cart(request):

    cart = request.session.get('cart', {})

    products = []

    subtotal = Decimal('0.00')


    for product_id, quantity in cart.items():

        product = get_object_or_404(
            Product,
            id=product_id
        )


        # Calculate individual product total

        total = product.price * quantity


        products.append({

            'product': product,

            'quantity': quantity,

            'total': total

        })


        # Add to subtotal

        subtotal += total


    # Delivery charge

    delivery_charge = Decimal('40.00')


    # Free delivery for orders above ₹500

    if subtotal >= Decimal('500.00'):

        delivery_charge = Decimal('0.00')


    # Grand total

    grand_total = subtotal + delivery_charge


    return render(

        request,

        'cart.html',

        {

            'products': products,

            'subtotal': subtotal,

            'delivery_charge': delivery_charge,

            'grand_total': grand_total

        }

    )


# INCREASE QUANTITY
def increase_quantity(request, id):

    cart = request.session.get('cart', {})

    id = str(id)


    if id in cart:

        cart[id] += 1


    request.session['cart'] = cart

    request.session.modified = True


    return redirect('cart')


# DECREASE QUANTITY
def decrease_quantity(request, id):

    cart = request.session.get('cart', {})

    id = str(id)


    if id in cart:

        if cart[id] > 1:

            cart[id] -= 1

        else:

            del cart[id]


    request.session['cart'] = cart

    request.session.modified = True


    return redirect('cart')


# REMOVE ITEM
def remove_from_cart(request, id):

    cart = request.session.get('cart', {})

    id = str(id)


    if id in cart:

        del cart[id]


    request.session['cart'] = cart

    request.session.modified = True


    return redirect('cart')


# CLEAR CART
def clear_cart(request):

    request.session['cart'] = {}

    request.session.modified = True


    return redirect('cart')

# CHECKOUT
def checkout(request):

    cart = request.session.get('cart', {})

    products = []

    subtotal = 0

    for product_id, quantity in cart.items():

        product = get_object_or_404(
            Product,
            id=product_id
        )

        total = product.price * quantity

        subtotal += total

        products.append({
            'product': product,
            'quantity': quantity,
            'total': total
        })

    # Delivery charge

    if subtotal >= 499:
        delivery_charge = 0
    else:
        delivery_charge = 40

    grand_total = subtotal + delivery_charge

    return render(
        request,
        'checkout.html',
        {
            'products': products,
            'subtotal': subtotal,
            'delivery_charge': delivery_charge,
            'grand_total': grand_total
        }
    )



   # LOGIN
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("home")

        else:

            messages.error(
                request,
                "Invalid username or password"
            )

    return render(request, "login.html")


# LOGOUT
def logout_view(request):

    logout(request)

    return redirect("home")

    # REGISTER
def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                "Username already exists"
            )

        else:

            User.objects.create_user(
                username=username,
                password=password
            )

            messages.success(
                request,
                "Registration successful. Please login."
            )

            return redirect("login")

    return render(request, "register.html")







@login_required
def dashboard(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    total_orders = Order.objects.filter(user=request.user).count()

    pending_orders = Order.objects.filter(
        user=request.user,
        status="Pending"
    ).count()

    delivered_orders = Order.objects.filter(
        user=request.user,
        status="Delivered"
    ).count()

    context = {
        "profile": profile,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "delivered_orders": delivered_orders,
    }

    return render(request, "dashboard.html", context)

@login_required
def profile(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        "profile.html",
        {
            "profile": profile
        }
    )


@login_required
def edit_profile(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        request.user.first_name = request.POST.get("first_name")
        request.user.email = request.POST.get("email")

        profile.phone = request.POST.get("phone")
        profile.address = request.POST.get("address")

        if request.FILES.get("profile_picture"):
            profile.profile_picture = request.FILES["profile_picture"]

        request.user.save()
        profile.save()

        messages.success(request, "Profile updated successfully.")

        return redirect("profile")

    return render(
        request,
        "edit_profile.html",
        {
            "profile": profile
        }
    )

@login_required
def orders(request):

    orders = (
        Order.objects
        .filter(user=request.user)
        .prefetch_related('items__product')
        .order_by('-created_at')
    )

    return render(request, 'orders.html', {
        'orders': orders
    })

@login_required
def change_password(request):

    if request.method == "POST":

        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect("change_password")

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect("change_password")

        request.user.set_password(new_password)
        request.user.save()

        # Keep the user logged in
        update_session_auth_hash(request, request.user)

        messages.success(request, "Password updated successfully.")

        return redirect("profile")

    return render(request, "change_password.html")

@login_required
def addresses(request):

    addresses = Address.objects.filter(user=request.user)

    return render(
        request,
        "addresses.html",
        {
            "addresses": addresses
        }
    )


@login_required
def add_address(request):

    if request.method == "POST":

        Address.objects.create(

            user=request.user,

            full_name=request.POST["full_name"],

            phone=request.POST["phone"],

            house=request.POST["house"],

            city=request.POST["city"],

            state=request.POST["state"],

            pincode=request.POST["pincode"]

        )

        messages.success(request, "Address Added Successfully")

        return redirect("addresses")

    return render(request, "add_address.html")



@login_required
def edit_address(request, id):

    address = get_object_or_404(
        Address,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        address.full_name = request.POST["full_name"]
        address.phone = request.POST["phone"]
        address.house = request.POST["house"]
        address.city = request.POST["city"]
        address.state = request.POST["state"]
        address.pincode = request.POST["pincode"]

        address.save()

        messages.success(request, "Address Updated")

        return redirect("addresses")

    return render(
        request,
        "edit_address.html",
        {
            "address": address
        }
    )

@login_required
def delete_address(request, id):

    address = get_object_or_404(
        Address,
        id=id,
        user=request.user
    )

    address.delete()

    messages.success(request, "Address Deleted")

    return redirect("addresses")



@login_required
def order_details(request, id):

    order = get_object_or_404(
        Order.objects.prefetch_related('items__product'),
        id=id,
        user=request.user
    )

    return render(request, 'order_details.html', {
        'order': order
    })


@login_required
def place_order(request):

    cart = request.session.get('cart', {})

    # Cart empty
    if not cart:
        return redirect('cart')

    if request.method == "POST":

        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        subtotal = Decimal('0.00')

        # =========================
        # CALCULATE SUBTOTAL
        # =========================
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            quantity = int(quantity)
            subtotal += product.price * quantity

        # =========================
        # DELIVERY CHARGE
        # =========================
        if subtotal >= Decimal('499.00'):
            delivery_charge = Decimal('0.00')
        else:
            delivery_charge = Decimal('40.00')

        # =========================
        # GRAND TOTAL
        # =========================
        grand_total = subtotal + delivery_charge

        # =========================
        # CREATE ORDER
        # =========================
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address=address,
            total=grand_total,
            status="Pending"
        )

        # =========================
        # CREATE ORDER ITEMS
        # =========================
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=int(quantity),
                price=product.price
            )

        # GET ORDER ITEMS
        order_items = OrderItem.objects.filter(order=order)

        # CLEAR CART
        request.session['cart'] = {}
        request.session.modified = True

        # SHOW SUCCESS PAGE
        context = {
            "full_name": order.full_name,
            "phone": order.phone,
            "address": order.address,
            "payment_method": payment_method,
            "subtotal": subtotal,
            "delivery_charge": delivery_charge,
            "grand_total": grand_total,
            "order_items": order_items,
        }

        return render(request, "order_success.html", context)

    return redirect('checkout')

@login_required
def cancel_order(request, id):

    if request.method == "POST":

        order = get_object_or_404(
            Order,
            id=id,
            user=request.user
        )

        # Only Pending orders can be cancelled
        if order.status == "Pending":

            order.status = "Cancelled"
            order.save()

    return redirect("order_details", id=id)



  

def fruits(request):

    products = Product.objects.filter(
        category__name="Fruits",
        available=True
    )

    search = request.GET.get("search")

    if search:
        products = products.filter(name__icontains=search)

    sort = request.GET.get("sort")

    if sort == "low":
        products = products.order_by("price")

    elif sort == "high":
        products = products.order_by("-price")

    elif sort == "new":
        products = products.order_by("-created")

    return render(request, "fruits.html", {
        "products": products
    })



def vegetables(request):
    products = Product.objects.filter(
        category__name__iexact="Vegetables",
        available=True
    )

    search = request.GET.get("search")
    if search:
        products = products.filter(name__icontains=search)

    sort = request.GET.get("sort")
    if sort == "low":
        products = products.order_by("price")
    elif sort == "high":
        products = products.order_by("-price")
    elif sort == "name":
        products = products.order_by("name")

    return render(request, "vegetables.html", {
        "products": products
    })
