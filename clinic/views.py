from django.shortcuts import render
from .models import Service

def index(request):
    return render(request, 'clinic/index.html')

def services(request):
    services = Service.objects.all()
    return render(request, 'clinic/services.html', {'services': services})

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
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RendezVousForm
from .models import RendezVous
from datetime import datetime

def prendre_rendezvous(request):
    if request.method == 'POST':
        form = RendezVousForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            
            # Vérifier si l'heure est déjà réservée pour cette date
            if RendezVous.objects.filter(date=date, time=time).exists():
                messages.error(request, 'L\'heure est déjà réservée pour cette date.')
            else:
                # Vérifier si la date est une nouvelle date (après aujourd'hui)
                if date >= datetime.today().date():
                    form.save()
                    messages.success(request, 'Rendez-vous enregistré avec succès!')
                else:
                    messages.error(request, 'La date doit être une nouvelle date.')
            
            return redirect('prendre_rendezvous')  # Redirect to the same page
    else:
        form = RendezVousForm()
    
    # Récupérez la liste des rendez-vous depuis la base de données et triez par date
    liste_rendezvous = RendezVous.objects.all().order_by('date')

    # Supprimez les rendez-vous expirés de la liste
    current_date = datetime.today().date()
    liste_rendezvous = [rdv for rdv in liste_rendezvous if rdv.date >= current_date]

    # Passez la liste des rendez-vous au modèle
    context = {'form': form, 'liste_rendezvous': liste_rendezvous}
    return render(request, 'clinic/rendezvous.html', context)




from django.shortcuts import redirect

def change_language(request, language_code):
    # Update the language session and redirect to the current page
    request.session['django_language'] = language_code
    return redirect(request.META.get('HTTP_REFERER'))
