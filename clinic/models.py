from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from PIL import Image

class RendezVous(models.Model):

    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255) 
    CIN = models.CharField(max_length=20)
    telephone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50, default="")
    date = models.DateField()
    time = models.CharField(max_length=5)
    presence = models.BooleanField()

    def __str__(self):
        return f"Rendez-vous with {self.nom} {self.prenom} on {self.telephone} {self.email} on {self.date} at {self.time}"
    

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    CIN = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100, default="")
    email = models.CharField(max_length=100, default="")
    date = models.DateField()
    time = models.TimeField()
    presence = models.BooleanField(default=False)

    def __str__(self):
        return f"Rendez-vous with {self.nom} {self.prenom} on {self.telephone} {self.email} on {self.date} at {self.time}"

class Service(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to='service_images')

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        return self.image.url if self.image else ''

@receiver(pre_save, sender=Service)
def service_pre_save(sender, instance, **kwargs):
    if instance.image:
        try:
            with Image.open(instance.image.path) as img:
                img.thumbnail((100, 100))
                img.save(instance.image.path, format='JPEG', quality=85)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error resizing image: {str(e)}")


class ServiceNoImage(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
           return self.name



