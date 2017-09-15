from django.db import models

#Reference tables
class Country(models.Model):
    codeA2 = models.CharField("ISO Alpha2 code",max_length=2, primary_key=True)
    codeA3 = models.CharField("ISO Alpha3 code",max_length=3)
    name = models.CharField("Country name",max_length=100)

    def __str__(self):
        return "%s (%s)" % (self.name,self.codeA2)

# Application
class Application(models.Model):
    name = models.CharField(max_length=50, unique=True)
    cryptoKey = models.CharField("Cryptographic key",max_length=200)
    icon = models.ImageField("Application icon",upload_to='appIcon')

    def __str__(self):
        return self.name

# Create your models here.
