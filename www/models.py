from django.db import models

# Application
class Application(models.Model):
    name = models.CharField(max_length=50, unique=True)
    cryptoKey = models.CharField("Cryptographic key",max_length=200)

    def __str__(self):
        return self.name

# Create your models here.
