from django import forms
from assosparents.models import Asso, EventNow, ConseilEcole, EventDurate, Partenaire, Message, Ressource

class CreateAsso(forms.ModelForm):
    class Meta:
        model = Asso
        fields = ('number',)

class SetAsso(forms.ModelForm):
    class Meta:
        model = Asso
        fields=('email', 'theme', 'minilogo', 'logo',)

        widgets = {
            'president': forms.TextInput(attrs={'class' : 'form-control mt-2'}),
            'email' : forms.EmailInput(attrs={'class' : 'form-control mt-2'}),
            'theme': forms.NumberInput(attrs={'class' : 'form-control mt-2'}),
        }

class CreateEventNow(forms.ModelForm):
    edit_EventNow = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    text = forms.CharField(widget = forms.Textarea)
    date_event = forms.DateField(widget = forms.SelectDateWidget)

    class Meta:
        model = EventNow
        exclude=['author', 'asso']
    
        widgets = {
            'title': forms.TextInput(attrs={'class' : 'form-control mt-2'}),
            'text': forms.TextInput(attrs={'class' : 'form-control mt-2'}),
            'date_event': forms.DateInput(attrs={'class' : 'form-control mt-2'}),
            'time_event': forms.TimeInput(attrs={'class' : 'form-control mt-2'}),
            'location': forms.TextInput(attrs={'class' : 'form-control mt-2'}),
        }

class DeleteEventNow(forms.Form):
    delete_EventNow = forms.BooleanField(widget=forms.HiddenInput, initial = True)

class CreateConseilEcole(forms.ModelForm):
    edit_ConseilEcole = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    date = forms.DateField(widget = forms.SelectDateWidget)
    resume = forms.CharField(widget = forms.Textarea)

    class Meta:
        model = ConseilEcole
        exclude = ['author', 'asso', ]
        
        widgets = {
        'date': forms.DateInput(attrs={'class' : 'form-control mt-2'}),
        'resume': forms.TextInput(attrs={'class' : 'form-control mt-2'}),
        }

class DeleteConseilEcole(forms.Form):
    Delete_ConseilEcole = forms.BooleanField(widget=forms.HiddenInput, initial = True)

class CreateEventDurate(forms.ModelForm):
    edit_EventDurate = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = EventDurate
        fields = ('day', 'title', 'text', 'time_event', 'location', 'file', 'image')

        widgets = {
        'title': forms.TextInput(attrs={'class' : 'form-control mt-2'}),
        'text': forms.TextInput(attrs={'class' : 'form-control mt-2'}),
        'time_event': forms.TimeInput(attrs={'class' : 'form-control mt-2'}),
        'location': forms.TextInput(attrs={'class' : 'form-control mt-2'}),
    }

class DeleteEventDurate(forms.Form):
    Delete_EventDurate = forms.BooleanField(widget=forms.HiddenInput, initial = True)

class CreatePartenaire(forms.ModelForm):
    edit_Partenaire = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = Partenaire
        fields = ('entreprise', 'promo_text', 'link', 'logo',)

        widgets = {
        'entreprise': forms.TextInput(attrs={'class' : 'form-control mt-2'}),
        'promo_text': forms.TextInput(attrs={'class' : 'form-control mt-2', 'placeholder' : '10€ de reduction avec le code promo ****'}),
        'link': forms.URLInput(attrs={'class' : 'form-control mt-2', 'placeholder' : 'https://www.sitedupartenaire.fr'}),
    }

class DeletePartenaire(forms.Form):
    Delete_Patenaire = forms.BooleanField(widget=forms.HiddenInput, initial = True)

class CreateMessage(forms.ModelForm):
    edit_Message = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = Message
        fields = ('title', 'text',)

        widgets = {
            'title': forms.TextInput(attrs={'class' : 'form-control mt-2'}),
            'text': forms.TextInput(attrs={'class' : 'form-control mt-2'}),
        }

class DeleteMessage(forms.Form):
    Delete_message = forms.BooleanField(widget=forms.HiddenInput, initial = True)

class CreateRessource(forms.ModelForm):
    edit_Ressource = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = Ressource
        fields = ('niveau', 'title', 'description', 'file', 'link',)

        widgets = {
            'title': forms.TextInput(attrs={'class' : 'form-control mt-2'}),
            'description': forms.TextInput(attrs={'class' : 'form-control mt-2'}),
            'link': forms.URLInput(attrs={'class' : 'form-control mt-2'}),
        }

class DeleteRessource(forms.Form):
    Delete_Ressource = forms.BooleanField(widget=forms.HiddenInput, initial = True)