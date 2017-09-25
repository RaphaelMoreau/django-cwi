from django.db import models

#Reference tables
class Country(models.Model):
    codeA2 = models.CharField("ISO Alpha2 code",max_length=2, primary_key=True)
    codeA3 = models.CharField("ISO Alpha3 code",max_length=3)
    name = models.CharField("Country name",max_length=100)
    display = models.BooleanField("Display country")

    def __str__(self):
        return "%s (%s)" % (self.name,self.codeA2)

class Platform(models.Model):
    name = models.CharField("Platform name", max_length=20)

    def __str__(self):
        return self.name

class AdType(models.Model):
    name = models.CharField("Ad type", max_length=20)

    def __str__(self):
        return self.name

class AdPlace(models.Model):
    name = models.CharField("Ad placement", max_length=20)

    def __str__(self):
        return self.name

# Application
class Application(models.Model):
    name = models.CharField(max_length=50, unique=True)
    cryptoKey = models.CharField("Cryptographic key",max_length=200)
    icon = models.ImageField("Application icon",upload_to='appIcon')

    def __str__(self):
        return self.name

# Application ad config (i.e. country) linked to an application
class ApplicationAdConfig(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    class Meta:
        unique_together = ('application', 'country',)

    def __str__(self):
        return "%s-%s" % (self.application.name,self.country.name)

# Application Platform, linked to an application configuration
class ApplicationPlatform(models.Model):
    config = models.ForeignKey(ApplicationAdConfig, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.PROTECT)
    class Meta:
        unique_together = ('config', 'platform')

    def __str__(self):
        return "%s-%s" % (self.config, self.platform.name)

# Application ad, linked to an application platform
class ApplicationAd(models.Model):
    platform = models.ForeignKey(ApplicationPlatform, on_delete=models.CASCADE)
    adType = models.ForeignKey(AdType, on_delete=models.PROTECT)
    adPlace = models.ForeignKey(AdPlace, on_delete=models.PROTECT)
    class Meta:
        unique_together = ('platform', 'adType', 'adPlace')

    def __str__(self):
        return "%s-%s-%s" % (self.platform, self.adType, self.adPlace)
