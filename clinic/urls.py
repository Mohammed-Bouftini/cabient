from django.urls import path
from . import views
from .views import get_rendezvous_data
urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('rendezvous/', views.rendezvous, name='rendezvous'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('prendre-rendezvous/', views.prendre_rendezvous, name='prendre_rendezvous'),
    path('change-language/<str:language_code>/', views.change_language, name='change_language'),
     path('get-rendezvous-data/', get_rendezvous_data, name='get_rendezvous_data'),

]
