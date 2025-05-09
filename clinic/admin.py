from django.contrib import admin
from django.utils import timezone
from .models import RendezVous,Contact# ,Service, ServiceNoImage
from PIL import Image
from django.urls import reverse
from django.utils.html import format_html
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer, Paragraph
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'subject','message', 'created_at']
    search_fields = ['name', 'email', 'phone', 'subject', 'message']
    list_filter = ['created_at']

@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom','CIN', 'telephone', 'email', 'date', 'time', 'presence', 'modify_button')
    list_filter = ('date', 'time')

    search_fields = ('nom','CIN' ,'prenom', 'telephone', 'email')

    ordering = ('date', 'time')
    
    actions = ['supprimer_rendezvous_expires', 'telecharger_rendezvous_pdf','toggle_presence']


    def toggle_presence(self, request, queryset):
        for rendezvous in queryset:
            rendezvous.presence = not rendezvous.presence
            rendezvous.save()
    toggle_presence.short_description = "Toggle Presence"  

    def supprimer_rendezvous_expires(self, request, queryset):
        current_date = timezone.now().date()
        expired_rendezvous = queryset.filter(date__lt=current_date)
        expired_rendezvous.delete()

        self.message_user(request, f"{len(expired_rendezvous)} rendez-vous expirés ont été supprimés.")

    supprimer_rendezvous_expires.short_description = "Supprimer les rendez-vous expirés"

    def modify_button(self, obj):
        change_url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html('<a href="{}">Modifier</a>', change_url)

    modify_button.short_description = 'Modifier'

    def telecharger_rendezvous_pdf(self, request, queryset):

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="rendezvous.pdf"'

   
        pdf = SimpleDocTemplate(response, pagesize=letter)


        logo_path = 'static/images/logopdf.png'  
        logo = Image(logo_path, width=70, height=70)
        logo.hAlign = 'CENTER'

        current_date = datetime.now().strftime('%Y-%m-%d')
        date_paragraph = Paragraph(f'<b>Date:</b> {current_date}', getSampleStyleSheet()['BodyText'])

        data = [['Nom', 'Prénom','CIN', 'Téléphone', 'Email', 'Date', 'Heure','Presence']]


        for rendezvous in queryset:
            presence = 'Oui' if rendezvous.presence else 'Non'
            data.append([rendezvous.nom,rendezvous.CIN , rendezvous.prenom, rendezvous.telephone, rendezvous.email,
                     str(rendezvous.date), str(rendezvous.time), presence])

        

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
    telecharger_rendezvous_pdf.short_description = "Télécharger les rendez-vous en PDF"


#@admin.register(Service)
#class ServiceAdmin(admin.ModelAdmin):
    #list_display = ('name', 'display_image', 'modify_button')
    #search_fields = ('name',)

    #def display_image(self, obj):
        #try:
            #if obj.image and hasattr(obj.image, 'path'):
             #   with Image.open(obj.image.path) as img:
            #        img.thumbnail((100, 100))
           #         return format_html('<img src="{}" width="{}" height="{}" />'.format(obj.image.url, img.width, img.height))
          #  else:
         #       return "Aucune image"
        #except FileNotFoundError:
       #     return "Image not found"
      #  except Exception as e:
     #       return f"Error displaying image: {str(e)}"

    #display_image.short_description = 'Image'

    #def modify_button(self, obj):
      #  change_url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
     #   return format_html('<a href="{}">Modifier</a>', change_url)

    #modify_button.short_description = 'Modifier' 


#@admin.register(ServiceNoImage)
#class ServiceNoImageAdmin(admin.ModelAdmin):
 #   list_display = ('name', 'modify_button')
  #  search_fields = ('name',)

   # def modify_button(self, obj):
    #    change_url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
     #   return format_html('<a href="{}">Modifier</a>', change_url)

    #modify_button.short_description = 'Modifier'



