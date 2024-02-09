from .models import Service,RendezVous ,ServiceNoImage
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RendezVousForm
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RendezVousSerializer,AdminSerializer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import HttpResponse ,JsonResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer,Paragraph
from django.contrib.auth.models import User
from django.core.serializers import serialize




def index(request):
    return render(request, 'clinic/index.html')

def services(request):
    services = Service.objects.all()
    servicesnoimages = ServiceNoImage.objects.all()
    return render(request, 'clinic/services.html', {'services': services , 'servicesnoimages':servicesnoimages})

def rendezvous(request):
    liste_rendezvous = RendezVous.objects.order_by('date')

    current_date = datetime.today().date()
    liste_rendezvous = [rdv for rdv in liste_rendezvous if rdv.date >= current_date]

    return render(request, 'clinic/rendezvous.html', {'liste_rendezvous': liste_rendezvous})



def contact(request):
    return render(request, 'clinic/contact.html')

def adminlogin(request):
    return render(request, 'clinic/adminlogin.html')



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



def change_language(request, language_code):
    request.session['django_language'] = language_code
    return redirect(request.META.get('HTTP_REFERER'))


def get_rendezvous_data(request):
    rendezvous_data = serialize('json', RendezVous.objects.all())
    return JsonResponse({'rendezvous_data': rendezvous_data})


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
    

class RendezVousApiViewID(APIView):
    def get(self, request, appointment_id, *args, **kwargs):
        try:
            rendezvous_instance = RendezVous.objects.get(id=appointment_id)
            serializer = RendezVousSerializer(rendezvous_instance)
            return Response({'rendezvousid_data': serializer.data}, status=status.HTTP_200_OK)
        except RendezVous.DoesNotExist:
            return Response({'error': 'RendezVous not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST', 'PUT', 'DELETE'])
def create_or_update_rendezvous(request, rendezvous_id=None):
    try:
        if request.method == 'POST':
            serializer = RendezVousSerializer(rendezvous, data=request.data, partial=True)

        elif request.method == 'PUT':
            rendezvous = RendezVous.objects.get(id=rendezvous_id)
            serializer = RendezVousSerializer(rendezvous, data=request.data)
        elif request.method == 'DELETE':

            rendezvous = RendezVous.objects.get(id=rendezvous_id)
            rendezvous.delete()
            return Response({"message": "Rendezvous deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except RendezVous.DoesNotExist:
        return Response({"error": "Rendezvous not found"}, status=status.HTTP_404_NOT_FOUND)

def generate_pdf(request):
    
    appointments = RendezVous.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rendezvous.pdf"'

    
    pdf = SimpleDocTemplate(response, pagesize=letter)
    logo_path = 'static/images/logopdf.png' 
    logo = Image(logo_path, width=70, height=70)
    logo.hAlign = 'CENTER'
    current_date = datetime.now().strftime('%Y-%m-%d')
    date_paragraph = Paragraph(f'<b>Date:</b> {current_date}', getSampleStyleSheet()['BodyText'])
    data = [['Nom', 'Prénom','CIN', 'Téléphone', 'Email', 'Date', 'Heure', 'Présence']]
    
    
    for appointment in appointments:
        
        presence = 'Oui' if appointment.presence else 'Non'
        data.append([appointment.nom, appointment.prenom,appointment.CIN, appointment.telephone, appointment.email, appointment.date, appointment.time, presence])

    elements = [Spacer(1, 1), logo, Spacer(1, 12), date_paragraph, Spacer(1, 12)] 

    table = Table(data)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table.setStyle(style)

    elements.append(table)
    pdf.build(elements)


    return response