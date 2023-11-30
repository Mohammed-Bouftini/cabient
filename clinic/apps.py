from django.apps import AppConfig



class ClinicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clinic'
    verbose_name = 'Cabinet Ouadie'

    def ready(self):
        # Importer la classe AdminConfig uniquement lorsque l'application est prête
        from django.contrib import admin

        # Définir l'icône pour le panneau d'administration
        admin.site.site_header = 'Cabinet Ouadie'
        admin.site.site_title = 'Cabinet Ouadie'
        admin.site.index_title = 'Gestion du Cabinet Ouadie'
        admin.site.site_icon = '{% static "images/favicon.ico" %}'  # Assurez-vous que le chemin est correct



