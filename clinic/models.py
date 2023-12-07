from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from PIL import Image
class RendezVous(models.Model):
    nom = models.CharField(max_length=100, default="")
    prenom = models.CharField(max_length=100, default="")
    CIN = models.CharField(max_length=100, default="")
    telephone = models.CharField(max_length=100, default="")
    email = models.CharField(max_length=100)
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
                img.save(instance.image.path)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error resizing image: {str(e)}")


class ServiceNoImage(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
           return self.name



