from django.shortcuts import render
from .models import Service
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RendezVousForm
from .models import RendezVous ,ServiceNoImage
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RendezVousSerializer

def index(request):
    return render(request, 'clinic/index.html')

def services(request):
    services = Service.objects.all()
    servicesnoimages = ServiceNoImage.objects.all()
    return render(request, 'clinic/services.html', {'services': services , 'servicesnoimages':servicesnoimages})

#def servicesnoimages(request):
   # servicesnoimages = ServiceNoImage.objects.all()
    #return render(request, 'clinic/services.html', {'servicesnoimages': servicesnoimages})

def rendezvous(request):
    # Récupérez tous les rendez-vous depuis la base de données et triez par date
    liste_rendezvous = RendezVous.objects.order_by('date')

    # Filtrez les rendez-vous expirés (antérieurs à la date actuelle)
    current_date = datetime.today().date()
    liste_rendezvous = [rdv for rdv in liste_rendezvous if rdv.date >= current_date]

    return render(request, 'clinic/rendezvous.html', {'liste_rendezvous': liste_rendezvous})



def contact(request):
    return render(request, 'clinic/contact.html')

def adminlogin(request):
    return render(request, 'clinic/adminlogin.html')

# views.py


def prendre_rendezvous(request):
    if request.method == 'POST':
        form = RendezVousForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            
            if RendezVous.objects.filter(date=date, time=time).exists():
                messages.error(request, 'L\'heure est déjà réservée pour cette date.')
            else:
                if date >= datetime.today().date():
                    form.save()
                    messages.success(request, 'Rendez-vous enregistré avec succès!')
                else:
                    messages.error(request, 'La date doit être une nouvelle date.')
            
            return redirect('prendre_rendezvous') 
    else:
        form = RendezVousForm()
    
    liste_rendezvous = RendezVous.objects.all().order_by('date')


    current_date = datetime.today().date()
    liste_rendezvous = [rdv for rdv in liste_rendezvous if rdv.date >= current_date]

    context = {'form': form, 'liste_rendezvous': liste_rendezvous}
    return render(request, 'clinic/rendezvous.html', context)




from django.shortcuts import redirect

def change_language(request, language_code):
    request.session['django_language'] = language_code
    return redirect(request.META.get('HTTP_REFERER'))


from django.http import JsonResponse
from .models import RendezVous
from django.core.serializers import serialize

def get_rendezvous_data(request):
    rendezvous_data = serialize('json', RendezVous.objects.all())
    return JsonResponse({'rendezvous_data': rendezvous_data})

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AdminSerializer
from django.contrib.auth.models import User

class AdminDataApiView(APIView):
    def get(self, request, *args, **kwargs):
        admins = User.objects.filter(is_superuser=True)
        serializer = AdminSerializer(admins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RendezVousApiView(APIView):
    def get(self, request, *args, **kwargs):
        rendezvous_data = RendezVous.objects.all()
        serializer = RendezVousSerializer(rendezvous_data, many=True)
        return Response({'rendezvous_data': serializer.data}, status=status.HTTP_200_OK)
    


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import RendezVousSerializer
from .models import RendezVous

@api_view(['POST', 'PUT', 'DELETE'])
def create_or_update_rendezvous(request, rendezvous_id=None):
    try:
        if request.method == 'POST':
            # Create a new rendezvous entry
            serializer = RendezVousSerializer(data=request.data)
        elif request.method == 'PUT':
            # Update an existing rendezvous entry
            rendezvous = RendezVous.objects.get(id=rendezvous_id)
            serializer = RendezVousSerializer(rendezvous, data=request.data)
        elif request.method == 'DELETE':
            # Delete an existing rendezvous entry
            rendezvous = RendezVous.objects.get(id=rendezvous_id)
            rendezvous.delete()
            return Response({"message": "Rendezvous deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except RendezVous.DoesNotExist:
        return Response({"error": "Rendezvous not found"}, status=status.HTTP_404_NOT_FOUND)
    

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from .models import RendezVous

def generate_pdf(request):
    # Fetch appointment data from the database
    appointments = RendezVous.objects.all()

    # Create a PDF file using ReportLab
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rendezvous.pdf"'

    # Create the PDF object
    pdf = SimpleDocTemplate(response, pagesize=letter)
    data = [['Nom', 'Prénom','CIN', 'Téléphone', 'Email', 'Date', 'Heure', 'Présence']]
    
    # Add content to the PDF based on appointment data
    for appointment in appointments:
        # Assuming 'presence' is a boolean field
        presence = 'Oui' if appointment.presence else 'Non'
        data.append([appointment.nom, appointment.prenom,appointment.CIN, appointment.telephone, appointment.email, appointment.date, appointment.time, presence])

    # Create a table and style
    table = Table(data)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    # Apply the style to the table
    table.setStyle(style)

    # Build the PDF with the table
    pdf.build([table])

    return response