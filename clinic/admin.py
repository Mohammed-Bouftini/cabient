from django.contrib import admin
from django.utils import timezone
from .models import RendezVous, Service
from PIL import Image
from django.utils.html import format_html

@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'telephone', 'email', 'date', 'time')
    list_filter = ('date', 'time')
    search_fields = ('nom', 'prenom', 'telephone', 'email')
    ordering = ('date', 'time')

    actions = ['supprimer_rendezvous_expires']

    def supprimer_rendezvous_expires(self, request, queryset):
        # Obtenez la date actuelle
        current_date = timezone.now().date()

        # Supprimez les rendez-vous dont la date est passée
        expired_rendezvous = queryset.filter(date__lt=current_date)
        expired_rendezvous.delete()

        self.message_user(request, f"{len(expired_rendezvous)} rendez-vous expirés ont été supprimés.")

    supprimer_rendezvous_expires.short_description = "Supprimer les rendez-vous expirés"
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_image')

    def display_image(self, obj):
        if obj.image:
            img = Image.open(obj.image.path)
            img.thumbnail((100, 100))  # Redimensionnez l'image à la taille souhaitée
            return format_html('<img src="{}" width="{}" height="{}" />'.format(obj.image.url, img.width, img.height))
        else:
            return "Aucune image"

    display_image.short_description = 'Image'
