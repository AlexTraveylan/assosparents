from django.db import models
from django.contrib.auth.models import AbstractUser
from assosparents.models import Asso, EventNow, Ressource, Message
from PIL import Image

class User(AbstractUser):
    profile_photo = models.ImageField(default='default_profile.png')
    asso=models.ManyToManyField(Asso, null = True, blank = True)
    eventnow=models.ManyToManyField(EventNow, null = True, blank = True)

    IMAGE_MAX_SIZE = (300, 300)
    
    def resize_profile_photo(self):
        image = Image.open(self.profile_photo)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.profile_photo.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_profile_photo()

class Role(models.Model):
    role = models.PositiveIntegerField(default = 1)
    asso = models.ForeignKey(Asso, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    class Meta:
        unique_together = ('asso', 'user',)

class Vote(models.Model):
    user_voteur = models.ForeignKey(User, related_name='voteur_user_set' ,on_delete = models.CASCADE)
    user_voted = models.ForeignKey(User, related_name='voted_user_set',on_delete = models.CASCADE)
    asso = models.ForeignKey(Asso, on_delete = models.CASCADE)

    class Meta:
        unique_together = ('asso', 'user_voteur',)

class MessageVu(models.Model):
    asso = models.ForeignKey(Asso, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    message = models.ForeignKey(Message, on_delete = models.CASCADE)

    class Meta:
        unique_together = ('message', 'user',)

class RessourceLike(models.Model):
    like = models.fields.BooleanField()
    asso = models.ForeignKey(Asso, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    ressource = models.ForeignKey(Ressource, on_delete = models.CASCADE)

    class Meta:
        unique_together = ('ressource', 'user',)