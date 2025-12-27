from django.urls import path
from django.views.i18n import set_language
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),
    path('menu/', views.menu_page, name='menu'),
    path('contact/', views.contact_page, name='contact'),
    path('privacy-policy/', views.privacy_policy_page, name='privacy_policy'),
    path('support/', views.support_page, name='support'),
    path('about/', views.about_page, name='about'),
    path('order/', views.order_create, name='order_create'),
    path('i18n/setlang/', set_language, name='set_language'),
]
