from django.contrib import admin
from authentication.models import User, Vote, Role
from assosparents.models import Asso,EventNow

# Register your models here.

admin.site.register(User)
admin.site.register(Asso)
admin.site.register(EventNow)
admin.site.register(Vote)
admin.site.register(Role)
