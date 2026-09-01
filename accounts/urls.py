from django.urls import path
from . import views


urlpatterns = [

    # Home
    path('', views.index, name='home'),

    # Categories
    path('fruits/', views.fruits, name='fruits'),
    path('vegetables/', views.vegetables, name='vegetables'),
    path('dairy/', views.dairy, name='dairy'),
  

    path("grocery/", views.grocery, name="grocery"),

    # Product
    path(
        'product/<int:id>/',
        views.product_details,
        name='product_details'
    ),

    

    # Cart
    path(
        'cart/',
        views.cart,
        name='cart'
    ),

    path(
        'cart/add/<int:id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/increase/<int:id>/',
        views.increase_quantity,
        name='increase_quantity'
    ),

    path(
        'cart/decrease/<int:id>/',
        views.decrease_quantity,
        name='decrease_quantity'
    ),

    path(
        'cart/remove/<int:id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    path(
        'cart/clear/',
        views.clear_cart,
        name='clear_cart'
    ),

    # Checkout
    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),

    path(
        'place-order/',
        views.place_order,
        name='place_order'
    ),

    # Authentication
    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
        'register/',
        views.register_view,
        name='register'
    ),

    # Dashboard
    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    # Profile
    path(
        'profile/',
        views.profile,
        name='profile'
    ),

    path(
        'profile/edit/',
        views.edit_profile,
        name='edit_profile'
    ),

    # Orders
    path(
        'orders/',
        views.orders,
        name='orders'
    ),

    path(
        'orders/<int:id>/',
        views.order_details,
        name='order_details'
    ),

    # Addresses
    path(
        'addresses/',
        views.addresses,
        name='addresses'
    ),

    path(
        'address/add/',
        views.add_address,
        name='add_address'
    ),

    path(
        'address/edit/<int:id>/',
        views.edit_address,
        name='edit_address'
    ),

    path(
        'address/delete/<int:id>/',
        views.delete_address,
        name='delete_address'
    ),

    # Change Password
    path(
        'change-password/',
        views.change_password,
        name='change_password'
    ),

    path(
    "orders/cancel/<int:id>/",
    views.cancel_order,
    name="cancel_order"
),
]