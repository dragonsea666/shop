from django.conf.urls import url
from order import views



urlpatterns = [

    url(r'^place_order/',views.place_order, name='place_order'),
    url(r'^user_center_order/',views.user_center_order, name='user_center_order'),
    url(r'^make_order/', views.make_order, name='make_order'),
]