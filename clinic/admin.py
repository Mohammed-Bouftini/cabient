from django.contrib import admin
from django.utils import timezone
from .models import RendezVous, Service, ServiceNoImage
from PIL import Image
from django.urls import reverse
from django.utils.html import format_html


@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'telephone', 'email', 'date', 'time', 'modify_button')
    list_filter = ('date', 'time')
    search_fields = ('nom', 'prenom', 'telephone', 'email')
    ordering = ('date', 'time')

    actions = ['supprimer_rendezvous_expires']

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


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_image', 'modify_button')
    search_fields = ('name',)

    def display_image(self, obj):
        try:
            if obj.image:
                with Image.open(obj.image.path) as img:
                    img.thumbnail((100, 100))
                    return format_html('<img src="{}" width="{}" height="{}" />'.format(obj.image.url, img.width, img.height))
            else:
                return "Aucune image"
        except FileNotFoundError:
            return "Image not found"
        except Exception as e:
            return f"Error displaying image: {str(e)}"


    display_image.short_description = 'Image'

    def modify_button(self, obj):
        change_url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html('<a href="{}">Modifier</a>', change_url)

    modify_button.short_description = 'Modifier'


@admin.register(ServiceNoImage)
class ServiceNoImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'modify_button')
    search_fields = ('name',)

    def modify_button(self, obj):
        change_url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html('<a href="{}">Modifier</a>', change_url)

    modify_button.short_description = 'Modifier'
