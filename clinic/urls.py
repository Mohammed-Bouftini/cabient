from django.urls import path
from . import views
from .views import AdminDataApiView
from .views import RendezVousApiView
<<<<<<< HEAD
from .views import RendezVousApiViewID
=======
>>>>>>> 242ae53128cdb93b4a04daa5eab8f623cf9e55e7
from .views import create_or_update_rendezvous
from .views import generate_pdf

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
<<<<<<< HEAD
    path('api/rendezvous/<int:appointment_id>/', RendezVousApiViewID.as_view(), name='rendezvous-api'),
=======
>>>>>>> 242ae53128cdb93b4a04daa5eab8f623cf9e55e7
    path('api/create_or_update_rendezvous/', create_or_update_rendezvous, name='create_or_update_rendezvous'),
    path('api/create_or_update_rendezvous/<int:rendezvous_id>/', views.create_or_update_rendezvous, name='create_or_update_rendezvous'),
    path('api/generate_pdf/', generate_pdf, name='generate_pdf'),
]
