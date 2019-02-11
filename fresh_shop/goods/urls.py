from django.conf.urls import url
from goods import views
# from rest_framework.routers import SimpleRouter
# router = SimpleRouter()
# router.register('goods', views.Goods)


urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^detail/(\d+)/', views.detail, name='detail'),
    url(r'^list/(\d+)/', views.list, name='list'),
    url(r'^search_list/', views.search_list,name='search_list'),
]

# urlpatterns += router.urls