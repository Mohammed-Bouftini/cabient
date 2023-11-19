from django.shortcuts import render
from .models import Service
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RendezVousForm
from .models import RendezVous ,ServiceNoImage
from datetime import datetime

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
