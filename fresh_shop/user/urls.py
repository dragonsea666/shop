from django.conf.urls import url
from user import views



urlpatterns = [
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^user_center_info/', views.user_center_info, name='user_center_info'),
    url(r'^user_center_site/',views.user_center_site, name='user_center_site',)

]