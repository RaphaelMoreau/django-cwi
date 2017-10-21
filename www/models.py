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

# Application countries linked to an application
class ApplicationCountry(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    class Meta:
        unique_together = ('application', 'country',)

    def __str__(self):
        return "%s-%s" % (self.application.name,self.country.name)

# Application Platform, linked to an application country
class ApplicationPlatform(models.Model):
    country = models.ForeignKey(ApplicationCountry, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.PROTECT)
    class Meta:
        unique_together = ('country', 'platform')

    def __str__(self):
        return "%s-%s" % (self.country, self.platform.name)

# Application ad type, linked to an application platform
class ApplicationAdType(models.Model):
    platform = models.ForeignKey(ApplicationPlatform, on_delete=models.CASCADE)
    adType = models.ForeignKey(AdType, on_delete=models.PROTECT)
    class Meta:
        unique_together = ('platform', 'adType')

    def __str__(self):
        return "%s-%s" % (self.platform, self.adType)

    def parameters(self):
        p = ApplicationAdTypeParameter.objects.filter(applicationAdType=self.id)
        return AdTypeParameter.objects.filter(adType=self.adType).prefetch_related(models.Prefetch("applicationadtypeparameter_set", queryset=p, to_attr='value'))

# application ad place, linked to an application platform and an application ad type
class ApplicationAdPlace(models.Model):
    platform = models.ForeignKey(ApplicationPlatform, on_delete=models.CASCADE)
    adType = models.ForeignKey(ApplicationAdType, on_delete=models.CASCADE)
    adPlace = models.ForeignKey(AdPlace, on_delete=models.PROTECT)
    class Meta:
        unique_together = ('platform', 'adType', 'adPlace')

    def __str__(self):
        return "%s-%s-%s" % (self.platform, self.adPlace, self.adType.adType)

#utility str to bool conversion function - private
def _str_to_bool(value):
    return value == 'True'

#Abstract class for parameters
class Parameter(models.Model):
    INTEGER = 1
    STRING = 2
    BOOLEAN = 3
    PERCENTAGE = 4
    TYPES_CHOICES = (
        (INTEGER, 'Integer'),
        (STRING, 'String'),
        (BOOLEAN, 'Boolean'),
        (PERCENTAGE, 'Percentage')
    )
    CONVERSIONS={
        INTEGER: ('Integer', int),
        STRING: ('String', str),
        BOOLEAN: ('Boolean', _str_to_bool),
        PERCENTAGE: ('Percentage', int),
    }
    name = models.CharField(max_length=45)
    type = models.IntegerField(choices=TYPES_CHOICES, default=INTEGER)
    mandatory = models.BooleanField()
    editable = models.BooleanField(default=True)
    default = models.CharField(max_length=100)
    helpText = models.CharField(max_length=200, null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super(Parameter, self).__init__(*args, **kwargs)
        self.type_text, self.convert = Parameter.CONVERSIONS.get(self.type)

    def effective_value(self):
        if self.editable:
            return self.convert(self.value[0].value if self.value else self.default)
        return self.convert(self.value[0].value if self.value else self.default)

    def _Update(self, value, parent):
        self.value[0].value = value
        self.value[0].save()
        return True

    def _Create(self, value, parent):
        kw = { self.parent_name: parent }
        p = ApplicationAdTypeParameter.objects.create(parameter=self, value=value, **kw)
        return True

    def _Remove(self, value, parent):
        self.value[0].delete()
        return True

    def _Ignore(self, value, parent):
        return False

    def store(self, value, parent):
        'Save value for parameter. Return True if changed, False otherwise'
        # the actions to perform depending on various conditions
        _actions = {
            'MEUN': self._Ignore,
            'MEUD': self._Ignore, #Do not store mandatory value same as default
            'MEUS': self._Ignore, #nonsense
            'MEUO': self._Create, #Create sub value
            'MESN': self._Remove, #Reset to default value by removing sub value
            'MESD': self._Remove, #Reset to default value by removing sub value
            'MESS': self._Ignore,
            'MESO': self._Update,
            'MFUN': self._Ignore,
            'MFUD': self._Ignore,
            'MFUS': self._Ignore, #nonsense
            'MFUO': self._Ignore, #That case should not happen. Just ignore it
            'MFSN': self._Remove, #No sub value should be stored on mandatory non editable parameters. So remove it
            'MFSD': self._Remove, #No sub value should be stored on mandatory non editable parameters. So remove it
            'MFSS': self._Remove, #No sub value should be stored on mandatory non editable parameters. So remove it
            'MFSO': self._Remove, #No sub value should be stored on mandatory non editable parameters. So remove it
            'OEUN': self._Ignore,
            'OEUD': self._Create,
            'OEUS': self._Ignore, #nonsense
            'OEUO': self._Create,
            'OESN': self._Remove,
            'OESD': self._Update,
            'OESS': self._Ignore,
            'OESO': self._Update,
            'OFUN': self._Ignore,
            'OFUD': self._Create,
            'OFUS': self._Create,
            'OFUO': self._Create,
            'OFSN': self._Remove,
            'OFSD': self._Update,
            'OFSS': self._Ignore,
            'OFSO': self._Update,
        }
        # get converted stored value and default value
        stored_value = self.convert(self.value[0].value) if self.value else None
        default = self.convert(self.default)
        # build a string to find the action to perform
        s = ('M' if self.mandatory else 'O')  # M if mandatory, O if optional
        s += ('E' if self.editable else 'F')  # E if editable, F if fixed
        s += ('S' if stored_value is not None else 'U')     # S if value is set, U if unset
        if value is None: # N if no value provided
            s += 'N'
        elif value == default: # D if provided value is same as default
            s += 'D'
        elif self.value and value == stored_value: # S if provided value is same as stored value if it exists
            s += 'S'
        else: # all other cases, i.e. provided value is different of default and different of stored value (if it exists)
            s += 'O'
        # Perform the action and return its value
        return _actions[s](value, parent)

    class Meta:
        abstract = True

# Ad types parameters
class AdTypeParameter(Parameter):
    adType = models.ForeignKey(AdType, on_delete=models.PROTECT)
    parent_name = 'applicationAdType'

    def __str__(self):
        return "%s-%s" % (self.adType, self.name)

class ApplicationAdTypeParameter(models.Model):
    applicationAdType = models.ForeignKey(ApplicationAdType)
    parameter = models.ForeignKey(AdTypeParameter)
    value = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return "%s-%s" % (self.applicationAdType, self.parameter)
