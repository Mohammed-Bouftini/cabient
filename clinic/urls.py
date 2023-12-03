from django.urls import path
from . import views
from .views import AdminDataApiView
from .views import RendezVousApiView

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('rendezvous/', views.rendezvous, name='rendezvous'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('prendre-rendezvous/', views.prendre_rendezvous, name='prendre_rendezvous'),
    path('change-language/<str:language_code>/', views.change_language, name='change_language'),
    path('get_rendezvous_data/', views.get_rendezvous_data, name='get_rendezvous_data'),
    path('api/admin_data_api/', AdminDataApiView.as_view(), name='admin_data_api'),
    path('api/rendezvous/', RendezVousApiView.as_view(), name='rendezvous_api'),
]
