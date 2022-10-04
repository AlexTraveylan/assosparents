from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image


class Photo(models.Model):
    ...
    IMAGE_MAX_SIZE = (800, 800)
    
    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        # sauvegarde de l’image redimensionnée dans le système de fichiers
        # ce n’est pas la méthode save() du modèle !
        image.save(self.image.path)


class Asso(models.Model):
    number=models.fields.CharField(max_length = 11, unique = 1)
    created=models.fields.CharField(max_length = 20, default = " ")
    name=models.fields.CharField(max_length = 150, default = " ")
    shortname=models.fields.CharField(max_length = 50, default = " ")
    objet=models.fields.CharField(max_length = 1000, default = " ")
    adress1=models.fields.CharField(max_length = 100, default = " ")
    adress2=models.fields.CharField(max_length = 100, default = " ")
    adress=models.fields.CharField(max_length = 100, default = " ")
    codepostal=models.fields.CharField(max_length = 10, default = " ")
    town=models.fields.CharField(max_length = 100, default = " ")
    pays=models.fields.CharField(max_length = 100, default = " ")
    president=models.fields.CharField(max_length = 50, default = "John Doh")
    verified=models.fields.BooleanField(default = False)
    minilogo=models.ImageField(default = 'default_profile.png')
    logo=models.ImageField(default = 'default_profile.png')
    email=models.fields.EmailField(max_length=200, blank=True, null=True)
    theme=models.fields.PositiveIntegerField(validators = [MinValueValidator(1),MaxValueValidator(9)], default = 1)

    IMAGE_MAX_SIZE = (600, 600)
    
    def resize_logo(self):
        image = Image.open(self.logo)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.logo.path)
    
    def resize_minilogo(self):
        image = Image.open(self.minilogo)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.minilogo.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_logo()
        self.resize_minilogo()

class EventNow(models.Model):
    title = models.fields.CharField(max_length = 200, default = "Pas de titre")
    text = models.fields.CharField(max_length = 4000)
    author = models.CharField(max_length = 150)
    time_published = models.DateTimeField(auto_now = True)
    date_event = models.DateField(default = '1970-01-01')
    time_event = models.TimeField()
    location = models.fields.CharField(max_length = 1000)
    file = models.FileField(null = True, blank = True)
    image = models.ImageField(null = True, blank = True)
    asso = models.ForeignKey(Asso, on_delete = models.CASCADE, blank = True, null = True)

    class Meta:
        unique_together = ('title', 'text', 'asso',)

    IMAGE_MAX_SIZE = (600, 600)
    
    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()

class ConseilEcole(models.Model):
    date = models.DateField()
    resume = models.fields.CharField(max_length = 6000)
    author = models.CharField(max_length = 150)
    time_published = models.DateTimeField(auto_now=True)
    file = models.FileField(null = True, blank = True)
    asso = models.ForeignKey(Asso, on_delete = models.CASCADE, blank = True, null = True)

    class Meta:
        unique_together = ('date', 'asso',)

class EventDurate(models.Model):
    DAYS_CHOICES = [
        ('LUNDIS' , 'Lundi'),
        ('MARDIS' , 'Mardi'),
        ('MERCREDIS' , 'Mercredi'),
        ('JEUDIS' , 'Jeudi'),
        ('VENDREDIS' , 'Vendredi'),
        ('SAMEDIS' , 'Samedi'),
        ('DIMANCHES' , 'Dimanche'),
    ]
    title = models.fields.CharField(max_length=200)
    text = models.fields.CharField(max_length=4000)
    day = models.CharField(max_length=10, choices=DAYS_CHOICES, default='LU')
    time_event = models.TimeField(null=True)
    location = models.fields.CharField(max_length = 1000, null=True)
    author = models.CharField(max_length=150)
    time_published = models.DateTimeField(auto_now=True)
    file = models.FileField(null = True, blank = True)
    image = models.ImageField(null = True, blank = True)
    asso = models.ForeignKey(Asso, on_delete = models.CASCADE, blank = True, null = True)

    class Meta:
        unique_together = ('title', 'text', 'asso',)

    IMAGE_MAX_SIZE = (600, 600)
    
    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()

class Partenaire(models.Model):
    entreprise = models.fields.CharField(max_length = 300)
    logo = models.ImageField()
    promo_text = models.fields.CharField(max_length=500, blank=True, null=True)
    link = models.URLField(max_length = 200, null = True, blank = True)
    asso = models.ForeignKey(Asso, on_delete = models.CASCADE, blank = True, null = True)

    class Meta:
        unique_together = ('entreprise', 'asso',)

    IMAGE_MAX_SIZE = (300, 300)
    
    def resize_logo(self):
        image = Image.open(self.logo)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.logo.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_logo()

class Message(models.Model):
    title = models.fields.CharField(max_length=200)
    text = models.fields.CharField(max_length=4000)
    asso = models.ForeignKey(Asso, on_delete = models.CASCADE, blank = True, null = True)

    class Meta:
        unique_together = ('title', 'asso',)

class Ressource(models.Model):
    LEVEL = [
        ('Maternelle' , 'Maternelle'),
        ('Élémentaire' , 'Elementaire'),
        ('Collège' , 'Collège'),
        ('Lycée' , 'Lycée'),
    ]
    title = models.fields.CharField(max_length=200)
    niveau = models.CharField(max_length=12, choices=LEVEL, default='Maternelle')
    description = models.fields.CharField(max_length=4000)
    file = models.FileField(null = True, blank = True)
    link = models.URLField(max_length = 200, null = True, blank = True)
    asso = models.ForeignKey(Asso, on_delete = models.CASCADE, blank = True, null = True)

    class Meta:
        unique_together = ('title', 'asso',)