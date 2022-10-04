"""assos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
import assosparents.views
import authentication.views
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', assosparents.views.index, name='index'),
    path('<int:id>/accueil',assosparents.views.accueil, name='accueil'),
    path('<int:id>/messages_create',assosparents.views.messages_create, name='messages_create'),
    path('<int:id>/<int:message_id>/messages_edit/', assosparents.views.messages_edit, name='messages_edit'),
    path('<int:id>/eventdurate',assosparents.views.eventdurate, name='eventdurate'),
    path('<int:id>/eventdurate_create',assosparents.views.eventdurate_create, name='eventdurate_create'),
    path('<int:id>/<int:event_id>/eventdurate_edit/', assosparents.views.eventdurate_edit, name='eventdurate_edit'),
    path('<int:id>/bemember',assosparents.views.bemember, name='bemember'),
    path('<int:id>/ressources',assosparents.views.ressources, name='ressources'),
    path('<int:id>/ressources_create',assosparents.views.ressources_create, name='ressources_create'),
    path('<int:id>/<int:ressource_id>/ressources_edit/', assosparents.views.ressources_edit, name='ressources_edit'),
    path('<int:id>/conseilsecole',assosparents.views.conseilsecole, name='conseilsecole'),
    path('<int:id>/conseilsecole_create',assosparents.views.conseilsecole_create, name='conseilsecole_create'),
    path('<int:id>/<int:conseil_id>/conseilsecole_edit/', assosparents.views.conseilsecole_edit, name='conseilsecole_edit'),
    path('<int:id>/donate',assosparents.views.donate, name='donate'),
    path('<int:id>/partenaires',assosparents.views.partenaires, name='partenaires'),
    path('<int:id>/partenaires_create',assosparents.views.partenaires_create, name='partenaires_create'),
    path('<int:id>/<int:partenaires_id>/partenaires_edit/', assosparents.views.partenaires_edit, name='partenaires_edit'),
    path('connect/', LoginView.as_view(template_name = 'login.html', redirect_authenticated_user = True), name = 'login'),
    path('logout/', LogoutView.as_view(template_name ='login.html'), name ='logout'),
    path('password_change/', PasswordChangeView.as_view(success_url='../password_change_done/'), name = 'passwordchange'),
    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name = 'passwordchangedone'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('photoprofil/upload', authentication.views.photoprofil_upload, name='photoprofil_upload'),
    path('verifasso/', assosparents.views.verifasso, name='verifasso'),
    path('confirmverifasso/', assosparents.views.confirmverifasso, name='confirmverifasso'),
    path('<int:id>/setting_asso/', assosparents.views.setting_asso, name='setting_asso'),
    path('<int:id>/eventnow',assosparents.views.EventNow_aff, name='eventnow'),
    path('<int:id>/<int:event_id>/eventnow_edit/', assosparents.views.EventNow_edit, name='eventnow_edit'),
    path('<int:id>/eventnow_create',assosparents.views.EventNow_create, name='eventnow_create'),
    path('<int:id>/eventpast',assosparents.views.EventPast, name='eventpast'),
    path('<int:id>/autorisation_required',assosparents.views.autorisation_required, name='autorisation_required'),
    path('<int:id>/election',assosparents.views.election, name='election'),
    
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
