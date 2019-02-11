
from django.conf.urls import url
from carts import views



urlpatterns = [

    url(r'^cart/', views.cart, name='cart'),
    url(r'^add_cart/', views.add_cart, name='add_cart'),
    url(r'^show_cart_count/', views.show_cart_count, name='show_cart_count'),
    url(r'^check_inventory/', views.check_inventory, name='check_inventory'),
    url(r'^change_cart/', views.change_cart, name='change_cart'),
    url(r'^del_cart/(\d+)/', views.del_cart, name='del_cart'),
    url(r'^change_all_cart/',views.change_all_cart,name='change_all_cart'),
]