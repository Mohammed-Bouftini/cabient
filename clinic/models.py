from django.db import models

class RendezVous(models.Model):
    nom = models.CharField(max_length=100, default="")
    prenom = models.CharField(max_length=100, default="")
    telephone = models.CharField(max_length=100, default="")
    email = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"Rendez-vous with {self.nom} {self.prenom} on {self.telephone} {self.email} on {self.date} at {self.time}"

class Service(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True)
    def __str__(self):
           return self.name
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

		



