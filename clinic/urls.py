from django.urls import path
from . import views
from .views import AdminDataApiView,RendezVousApiView,RendezVousApiViewID,create_or_update_rendezvous,generate_pdf
from django.urls import path
from django.conf.urls import handler404

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('rendezvous/', views.rendezvous, name='rendezvous'),
    path('prendre-rendezvous/', views.prendre_rendezvous, name='prendre_rendezvous'),
    path('contact/', views.contact, name='contact'),
    path('change-language/<str:language_code>/', views.change_language, name='change_language'),
    path('get_rendezvous_data/', views.get_rendezvous_data, name='get_rendezvous_data'),
    path('api/admin_data_api/', AdminDataApiView.as_view(), name='admin_data_api'),
    path('api/rendezvous/', RendezVousApiView.as_view(), name='rendezvous_api'),
    path('api/rendezvous/<int:appointment_id>/', RendezVousApiViewID.as_view(), name='rendezvous-api'),
    path('api/create_or_update_rendezvous/', create_or_update_rendezvous, name='create_or_update_rendezvous'),
    path('api/create_or_update_rendezvous/<int:rendezvous_id>/', views.create_or_update_rendezvous, name='create_or_update_rendezvous'),
    path('api/generate_pdf/', generate_pdf, name='generate_pdf'),
]
handler404 = "clinic.views.handel404"