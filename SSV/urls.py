from django.urls import path
from SSV import views
from django.conf.urls import url

urlpatterns = [

    url('admin_about', views.admin_about, name='admin_about'),
    url('admin_statistics', views.admin_statistics, name='admin_statistics'),
    url('admin_result', views.admin_result, name='admin_result'),
    url('code', views.code, name='code'),
    url('admin_add_subject', views.admin_add_subject, name='admin_add_subject'),
    url('admin_view_subject', views.admin_view_subject, name='admin_view_subject'),
    url('admin_index', views.admin_index, name='admin_index'),
    url('admin_login', views.admin_login, name='admin_login'),
    url('index', views.index, name='index'),
    url('login', views.user_login, name='user_login'),
    url('forgot-password', views.forgot_password, name='forgot-password'),
    url('about-us', views.about_us, name='about-us'),
    url('statistics', views.statistics, name='statistics'),
    url('contact-us', views.contact_us, name='contact-us'),
    url('logout', views.user_logout, name='user_logout'),
    url('thankyou', views.thankyou, name='thankyou'),
    url('registration', views.registration, name='registration'),
    url('edit_profile', views.edit_profile, name='edit_profile'),
    url('profile', views.profile, name='profile'),
    url('change_password', views.change_password, name='change_password'),
    url('change', views.change, name='change'),
    url('user_logout', views.user_logout, name='user_logout'),
 
]
