from ast import Delete
from django.shortcuts import render, redirect
from assosparents.models import *
from authentication.models import *
from assosparents.forms import *
from django.contrib.auth.decorators import login_required
from . import fonctions
from django.shortcuts import get_object_or_404
from datetime import datetime

#REVOIR LE SYSTEME D'AUTORISATIONS QUAND MEILLEURE COMPREHENSION DES DECORATEURS

def index(request):
    asso = Asso.objects.all()
    if request.method =='POST':
        RNA=request.POST['RNA']
        datas=fonctions.recupasso(RNA)
        if datas[0]:
            #pas opti a refaire
            tempasso=[]
            tempasso.append(RNA)
            tempasso.append(datas[1])
            tempasso.append(datas[2])
            tempasso.append(datas[3])
            tempasso.append(datas[4])
            tempasso.append(datas[5])
            tempasso.append(datas[6])
            tempasso.append(datas[7])
            tempasso.append(datas[8])
            tempasso.append(datas[9])
            tempasso.append(datas[10])     
            return render(request, 'verifasso.html', {'tempasso': tempasso, 'RNA' : RNA})
        else:
            message='echec'
            return render(request, 'index.html', {'asso': asso, 'message':message})
    return render(request, 'index.html', {'asso': asso})

def verifasso(request):
    message='Pas de message'
    if request.method == 'POST':
        #pas opti a refaire
        number=request.POST['number']
        created=request.POST['created']
        name=request.POST['name']
        shortname=request.POST['shortname']
        objet=request.POST['objet']
        adress1=request.POST['adress1']
        adress2=request.POST['adress2']
        adress=request.POST['adress']
        codepostal=request.POST['codepostal']
        town=request.POST['town']
        pays=request.POST['pays']
        if request.POST['btn-submit'] == "Oui":
            newasso=Asso()
            newasso.number=number
            newasso.created=created
            newasso.name=name
            newasso.shortname=shortname
            newasso.objet=objet
            newasso.adress1=adress1
            newasso.adress2=adress2
            newasso.adress=adress
            newasso.codepostal=codepostal
            newasso.town=town
            newasso.pays=pays
            try:
                newasso.save()
                message = "L'association a bien été crée"
            except:
                message="Cette association existe deja dans la base de donnée"
            return render(request, 'confirmverifasso.html', {'message' : message})
        else :
            message = "Ok, annulation"
            return render(request, 'confirmverifasso.html', {'message' : message})

def confirmverifasso(request):
    return render(request, 'confirmverifasso.html')
    

def accueil(request, id):
    asso=Asso.objects.get(id=id)
    messages = Message.objects.all().filter(asso=asso)
    if request.method == 'POST':
        if 'Vu_pushed' in request.POST:
            message_id=int(request.POST['Vu_pushed'])
            message = Message.objects.get(id = message_id)
            try:
                check_vu = MessageVu.objects.get(asso = asso, message = message, user = request.user)
                check_vu.delete()
            except:
                create_vu = MessageVu()
                create_vu.message = message
                create_vu.asso = asso
                create_vu.user = request.user
                create_vu.save()
    datas = []
    #datas [[]] avec pour chaque élement :
        #0 -> message
        #1 -> nombre de vu du message
        #2 -> couleur du bouton
    for message in messages:
        data = []
        data.append(message)
        nbvus = MessageVu.objects.all().filter(asso=asso, message=message).count()
        data.append(nbvus)
        try:
            check_vu = MessageVu.objects.get(asso = asso, message = message, user = request.user)
            color = 'text-light'
        except:
            color = 'text-1'
        data.append(color)
        datas.append(data)
    try :
        role = Role.objects.get(asso = asso, user = request.user)
        role = role.role
    except:
        role = 1
    return render(request,'accueil.html', {'asso' : asso, 'role' : role, 'messages' : datas})

@login_required
def messages_create(request, id):
    asso = Asso.objects.get(id = id)
    try :
        role = Role.objects.get(asso = asso, user = request.user)
        role = role.role
    except:
        role = 1
    if role > 2:
        form = CreateMessage()
        if request.method == 'POST':
            form = CreateMessage(request.POST, request.FILES)
            if form.is_valid():
                part = form.save(commit = False)
                part.asso = asso
                part.save()
                return redirect('accueil', id)
        return render(request, 'messages_create.html', {'asso' : asso, 'form' : form, 'role' : role})
    else :
        return redirect('autorisation_required', id)

@login_required
def messages_edit(request, id, message_id):
    asso = Asso.objects.get(id = id)
    try :
        role = Role.objects.get(asso = asso, user = request.user)
        role = role.role
    except:
        role = 1
    if role > 2:
        message = get_object_or_404(Message, id = message_id)
        edit_form = CreateMessage(instance = message)
        delete_form = DeleteMessage()
        if request.method == 'POST':
            if 'edit_Message' in request.POST:
                edit_form = CreateMessage(request.POST, request.FILES, instance = message)
                if edit_form.is_valid():
                    edit_form.save()
                    delete_vus = MessageVu.objects.all().filter(asso = asso, message = message)
                    for vu in delete_vus:
                        vu.delete()
                return redirect('accueil', id)
            if 'Delete_message' in request.POST:
                delete_form = DeleteMessage(request.POST)
                if delete_form.is_valid():
                    message.delete()
                    return redirect('accueil', id)
        context = {
            'asso' : asso,
            'edit_form' : edit_form,
            'delete_form' : delete_form,
            'role' : role,
        }
        return render(request, 'messages_edit.html', context)
    else :
        return redirect('autorisation_required', id)

@login_required
def EventNow_create(request, id):
    message='Aucun message'
    asso = Asso.objects.get(id=id)
    try :
        role = Role.objects.get(asso = asso, user = request.user)
        role = role.role
    except:
        role = 1
    if role > 2:
        form = CreateEventNow()
        if request.method == 'POST':
            form = CreateEventNow(request.POST, request.FILES)
            if form.is_valid():
                event = form.save(commit=False)
                event.asso=asso
                event.author = request.user.username
                event.save()
                message = 'réussi'
                return redirect('eventnow', id)
            else:
                message='raté'
        return render(request,'eventnow_create.html', {'message' : message, 'asso' : asso, 'form' : form, 'role' : role})
    else :
        redirect('autorisation_required', id)

def EventPast(request, id):
    test = "coucou"
    asso = Asso.objects.get(id = id)
    try :
        role = Role.objects.get(asso = asso, user = request.user)
        role = role.role
    except:
        role = 1
    starttime="2000-01-01"
    endtime=datetime.today()
    events = EventNow.objects.all().filter(asso=asso, date_event__range = [starttime, endtime])
    test = "0"
    datas = []
    test = "1"
    #tableau de tableaux avec pour chaque array : 
    #0 -> event 
    #1 -> participants
    i=2
    for event in events:
        tab = []
        participants = event.user_set.all()
        tab.append(event)
        tab.append(participants)
        datas.append(tab)
        test = i
        i=i+1
    return render(request, 'eventpast.html', {'asso' : asso, 'datas' : datas, 'test' : test, 'role' : role})

def EventNow_aff(request, id):
    asso = Asso.objects.get(id=id)
    try :
        role = Role.objects.get(asso = asso, user = request.user)
        role = role.role
    except:
        role = 1
    datas = []
    #tableau de tableaux avec pour chaque array : 
    #0 -> event 
    #1 -> participants
    #2 -> message pour le bouton
    starttime = datetime.today()
    endtime = "3000-01-01"
    events = EventNow.objects.all().filter(asso=asso, date_event__range = [starttime, endtime])
    for event in events:
        tab=[]
        tab.append(event)
        #event en 0
        participants = event.user_set.all()
        tab.append(participants)
        #participants en 1
        if request.user in participants:
            btn_message = 'Ne plus participer'
        else:
            btn_message = "Participer"
        tab.append(btn_message)
        #btn_message en 2
        datas.append(tab)
        #validation dans data
    i=0
    if request.method == 'POST':
        for event in events:
            if str(event.id) in request.POST:
                if event in request.user.eventnow.all():
                    request.user.eventnow.remove(event)
                    datas[i][2]= 'Participer'
                else:
                    request.user.eventnow.add(event)
                    datas[i][2] = 'Ne plus participer'
                datas[i][1] = event.user_set.all()
            i+=1
    return render(request, 'eventnow.html', {'asso' : asso, 'datas' : datas, 'role' : role})

@login_required
def EventNow_edit(request, id, event_id):
    asso = Asso.objects.get(id = id)
    try :
        role = Role.objects.get(asso = asso, user = request.user)
        role = role.role
    except:
        role = 1
    if role > 2:
        event = get_object_or_404(EventNow, id = event_id)
        edit_form = CreateEventNow(instance = event)
        delete_form = DeleteEventNow()
        if request.method == 'POST':
            if 'edit_EventNow' in request.POST:
                edit_form = CreateEventNow(request.POST, request.FILES, instance = event)
                if edit_form.is_valid():
                    edit_form.save()
                return redirect('eventnow', id)
            if 'delete_EventNow' in request.POST:
                delete_form = DeleteEventNow(request.POST)
                if delete_form.is_valid():
                    event.delete()
                    return redirect('eventnow', id)
        context = {
            'asso' : asso,
            'edit_form' : edit_form,
            'delete_form' : delete_form,
            'role' : role
        }
        return render(request, 'eventnow_edit.html', context)
    else :
        return redirect('autorisation_required', id)

@login_required
def eventdurate_edit(request, id, event_id):
    asso = Asso.objects.get(id = id)
    try :
        role = Role.objects.get(asso = asso, user = request.user)
        role = role.role
    except:
        role = 1
    if role > 2:
        event = get_object_or_404(EventDurate, id = event_id)
        edit_form = CreateEventDurate(instance = event)
        delete_form = DeleteEventDurate()
        if request.method == 'POST':
            if 'edit_EventDurate' in request.POST:
                edit_form = CreateEventDurate(request.POST, request.FILES, instance = event)
                if edit_form.is_valid():
                    edit_form.save()
                return redirect('eventdurate', id)
            if 'Delete_EventDurate' in request.POST:
                delete_form = DeleteEventDurate(request.POST)
                if delete_form.is_valid():
                    event.delete()
                    return redirect('eventdurate', id)
        context = {
            'asso' : asso,
            'edit_form' : edit_form,
            'delete_form' : delete_form,
            'role' : role,
        }
        return render(request, 'eventdurate_edit.html', context)
    else :
        return redirect('autorisation_required', id)


def eventdurate(request, id):
    asso = Asso.objects.get(id=id)
    try :
        role = Role.objects.get(asso = asso, user = request.user)
        role = role.role
    except:
        role = 1
    datas = EventDurate.objects.all().filter(asso = asso)
    return render(request,'eventdurate.html', {'asso' : asso, 'datas' : datas, 'role' : role})

@login_required
def eventdurate_create(request, id):
    asso = Asso.objects.get(id = id)
    try :
        role = Role.objects.get(asso = asso, user = request.user)
        role = role.role
    except:
        role = 1
    if role > 2:
        form = CreateEventDurate()
        if request.method == 'POST':
            form = CreateEventDurate(request.POST, request.FILES)
            if form.is_valid():
                event = form.save(commit = False)
                event.author = request.user.username
                event.asso = asso
                event.save()
                return redirect('eventdurate', id)
        return render(request, 'eventdurate_create.html', {'asso' : asso, 'form' : form, 'role' : role})
    else :
        return redirect('autorisation_required', id)


@login_required
def bemember(request, id):
    asso = Asso.objects.get(id=id)
    members = asso.user_set.all()
    if request.user in members:
        btn_message = 'Quitter l\'association'
    else:
        btn_message = 'Rejoindre l\'assocation'
    if request.method == 'POST':
        if request.user in members:
            request.user.asso.remove(asso)
            try :
                unset_vote = Vote.objects.get(asso = asso, user_voteur = request.user)
                unset_vote.delete()
            except:
                pass
            try:
                others_vote = Vote.objects.all().filter(asso=asso, user_voted = request.user)
                for vote in others_vote:
                    vote.delete()
            except:
                pass
            try:
                unset_role = Role.objects.get(asso = asso, user = request.user)
                unset_role.delete()
            except:
                pass
            btn_message = 'Rejoindre l\'assocation'
        else:
            request.user.asso.add(asso)
            set_role = Role()
            set_role.role = 2
            set_role.asso = asso
            set_role.user = request.user
            set_role.save()
            btn_message = 'Quitter l\'association'
        members = asso.user_set.all()
    try :
        role = Role.objects.get(asso = asso, user = request.user)
        role = role.role
    except:
        role = 1
    return render(request,'bemember.html', {'asso' : asso, 'btn_message' : btn_message, 'members' : members, 'role' : role})

def election(request, id):
    asso = Asso.objects.get(id = id)
    try :
        role = Role.objects.get(asso = asso, user = request.user)
        role = role.role
    except:
        role = 1
    members = asso.user_set.all()
    #PAS OPTI
    results=[]
        #array d'array avec pour chaque case
        #0 obj membre
        #1 nb de vote sur lui 
    for member in members:
        nbvote = asso.vote_set.all().filter(user_voted = member).count()
        results.append([member, nbvote])
    if asso.verified == False:
        message=''
        if request.method == 'POST':
            if 'target' in request.POST:
                username = request.POST['target']
                try:
                    vote = Vote.objects.get(user_voteur = request.user, asso = asso)
                except:
                    vote = Vote()
                    vote.user_voteur = request.user
                    vote.asso = asso
                vote.user_voted = User.objects.get(username = username)
                vote.save()
            results=[]
            #array d'array avec pour chaque case
            #0 obj membre
            #1 nb de vote sur lui 
            for member in members:
                nbvote = asso.vote_set.all().filter(user_voted = member).count()
                results.append([member, nbvote])
            if 'EndVote' in request.POST:
                nbvotetotal = asso.vote_set.all().count()
                nbmember = members.count()
                if nbvotetotal > 2:
                    if nbvotetotal > nbmember/2:
                        max_vote = None
                        for compteur in results:
                            if (max_vote is None or compteur[1] > max_vote):
                                max_vote = compteur[1]
                                vainqueur = compteur[0]
                        message=f'Le président est {vainqueur} avec {max_vote} votes'
                        asso.president=f'{vainqueur.first_name} {vainqueur.last_name}'
                        asso.verified = True
                        asso.save()
                        role = Role.objects.get(asso=asso, user=vainqueur)
                        role.role=4
                        role.save()
                    else:
                        message = f'Il y a {nbmember} qui ont rejoint l\'association, seulement {nbvotetotal} ont voté, c\'est moins que la moitié'
                else :
                    message = f'Seulement {nbvotetotal} vote(s) enregistré(s), il en faut minimum 3'
    else:
        message = f'Fin du vote, le président {asso.president} est elu'
        if request.method == 'POST':
            if 'reinitialiser' in request.POST:
                if request.POST['reinitialiser'] == 'confirme':
                    asso.verified = False
                    asso.president = "Le président a démissionné"
                    asso.save()
                    all_role = Role.objects.all().filter(asso = asso)
                    all_vote = Vote.objects.all().filter(asso = asso)
                    for vote in all_vote:
                        vote.delete()
                    for role in all_role:
                        role.role = 2
                        role.save()
                    

    return render(request,'election.html', {'asso' : asso, 'results' : results, 'message' : message, 'role' : role})


def ressources(request, id):
    asso = Asso.objects.get(id = id)
    ressources = Ressource.objects.all().filter(asso=asso)
    if request.method == 'POST':
        if 'like' in request.POST:
            ressource_id = int(request.POST['ressource_id'])
            ressource = Ressource.objects.get(id = ressource_id)
            try:
                check_like = RessourceLike.objects.get(asso = asso, ressource = ressource, user = request.user)
                if check_like.like:
                    check_like.delete()
                else:
                    check_like.like = True
                    check_like.save()
            except:
                create_like = RessourceLike()
                create_like.like = True
                create_like.asso = asso
                create_like.user = request.user
                create_like.ressource = ressource
                create_like.save()
        elif 'unlike' in request.POST:
            ressource_id = int(request.POST['ressource_id'])
            ressource = Ressource.objects.get(id = ressource_id)
            try:
                check_like = RessourceLike.objects.get(asso = asso, ressource = ressource, user = request.user)
                if check_like.like:
                    check_like.like = False
                    check_like.save()
                else:
                    check_like.delete()
            except:
                create_like = RessourceLike()
                create_like.like = False
                create_like.asso = asso
                create_like.user = request.user
                create_like.ressource = ressource
                create_like.save()
    datas = []
    #datas -> [[]] avec pour chaque élément :
        #0 -> ressource
        #1 -> [nombre de like, nombre de dislike]
        #2 -> [couleur du bouton like, couleur du bouton dislike]
    for ressource in ressources:
        data = []
        data.append(ressource)
        nblike = RessourceLike.objects.all().filter(asso=asso, ressource=ressource, like = True).count()
        nbdislike = RessourceLike.objects.all().filter(asso=asso, ressource=ressource, like = False).count()
        data.append([nblike, nbdislike])
        try:
            check_like = RessourceLike.objects.get(asso = asso, ressource = ressource, user = request.user, like = True)
            color_like = 'text-light'
        except:
            color_like = 'text-1'
        try:
            check_dislike = RessourceLike.objects.get(asso = asso, ressource = ressource, user = request.user, like = False)
            color_dislike = 'text-5'
        except:
            color_dislike = 'text-1'
        data.append([color_like,color_dislike])
        datas.append(data)
    try :
        role = Role.objects.get(asso = asso, user = request.user)
        role = role.role
    except:
        role = 1
    return render(request,'ressources.html', {'asso' : asso, 'role' : role, 'datas' : datas})

@login_required
def ressources_create(request, id):
    asso = Asso.objects.get(id = id)
    try :
        role = Role.objects.get(asso = asso, user = request.user)
        role = role.role
    except:
        role = 1
    if role > 2:
        form = CreateRessource()
        if request.method == 'POST':
            form = CreateRessource(request.POST, request.FILES)
            if form.is_valid():
                part = form.save(commit = False)
                part.asso = asso
                part.save()
                return redirect('ressources', id)
        return render(request, 'ressources_create.html', {'asso' : asso, 'form' : form, 'role' : role})
    else :
        return redirect('autorisation_required', id)

@login_required
def ressources_edit(request, id, ressource_id):
    asso = Asso.objects.get(id = id)
    try :
        role = Role.objects.get(asso = asso, user = request.user)
        role = role.role
    except:
        role = 1
    if role > 2:
        ressource = get_object_or_404(Ressource, id = ressource_id)
        edit_form = CreateRessource(instance = ressource)
        delete_form = DeleteRessource()
        if request.method == 'POST':
            if 'edit_Ressource' in request.POST:
                edit_form = CreateRessource(request.POST, request.FILES, instance = ressource)
                if edit_form.is_valid():
                    edit_form.save()
                    delete_like_dislike = RessourceLike.objects.all().filter(asso = asso, ressource = ressource)
                    for like in delete_like_dislike:
                        like.delete()
                return redirect('ressources', id)
            if 'Delete_Ressource' in request.POST:
                delete_form = DeleteRessource(request.POST)
                if delete_form.is_valid():
                    ressource.delete()
                    return redirect('ressources', id)
        context = {
            'asso' : asso,
            'edit_form' : edit_form,
            'delete_form' : delete_form,
            'role' : role,
        }
        return render(request, 'ressources_edit.html', context)
    else :
        return redirect('autorisation_required', id)

def conseilsecole(request, id):
    asso=Asso.objects.get(id=id)
    try :
        role = Role.objects.get(asso = asso, user = request.user)
        role = role.role
    except:
        role = 1
    datas = ConseilEcole.objects.all().filter(asso = asso)
    return render(request,'conseilsecole.html', {'asso' : asso, 'datas' : datas, 'role' : role})

@login_required
def conseilsecole_create(request, id):
    asso = Asso.objects.get(id = id)
    try :
        role = Role.objects.get(asso = asso, user = request.user)
        role = role.role
    except:
        role = 1
    if role > 2:
        form = CreateConseilEcole()
        if request.method == 'POST':
            form = CreateConseilEcole(request.POST, request.FILES)
            if form.is_valid():
                conseilecole = form.save(commit = False)
                conseilecole.asso = asso
                conseilecole.author = request.user.username
                conseilecole.save()
                return redirect('conseilsecole', id)
        return render(request, 'conseilsecole_create.html', {'asso' : asso, 'form' : form, 'role' : role})
    else :
        return redirect('autorisation_required', id)

@login_required
def conseilsecole_edit(request, id, conseil_id):
    asso = Asso.objects.get(id = id)
    try :
        role = Role.objects.get(asso = asso, user = request.user)
        role = role.role
    except:
        role = 1
    if role > 2:
        conseil = get_object_or_404(ConseilEcole, id = conseil_id)
        edit_form = CreateConseilEcole(instance = conseil)
        delete_form = DeleteConseilEcole()
        if request.method == 'POST':
            if 'edit_ConseilEcole' in request.POST:
                edit_form = CreateConseilEcole(request.POST, request.FILES, instance = conseil)
                if edit_form.is_valid():
                    edit_form.save()
                return redirect('conseilsecole', id)
            if 'Delete_ConseilEcole' in request.POST:
                delete_form = DeleteConseilEcole(request.POST)
                if delete_form.is_valid():
                    conseil.delete()
                    return redirect('conseilsecole', id)
        context = {
            'asso' : asso,
            'edit_form' : edit_form,
            'delete_form' : delete_form,
            'role' : role,
        }
        return render(request, 'conseilsecole_edit.html', context)
    else :
        return redirect('autorisation_required', id)

    
def donate(request, id):
    asso=Asso.objects.get(id=id)
    try :
        role = Role.objects.get(asso = asso, user = request.user)
        role = role.role
    except:
        role = 1
    return render(request,'donate.html', {'asso' : asso, 'role' : role})


def partenaires(request, id):
    asso = Asso.objects.get(id=id)
    try :
        role = Role.objects.get(asso = asso, user = request.user)
        role = role.role
    except:
        role = 1
    datas = Partenaire.objects.all().filter(asso = asso)
    return render(request,'partenaires.html', {'asso' : asso, 'datas' : datas, 'role' : role})

@login_required
def partenaires_create(request, id):
    asso = Asso.objects.get(id = id)
    try :
        role = Role.objects.get(asso = asso, user = request.user)
        role = role.role
    except:
        role = 1
    if role > 2:
        form = CreatePartenaire()
        if request.method == 'POST':
            form = CreatePartenaire(request.POST, request.FILES)
            if form.is_valid():
                part = form.save(commit = False)
                part.asso = asso
                part.save()
                return redirect('partenaires', id)
        return render(request, 'partenaires_create.html', {'asso' : asso, 'form' : form, 'role' : role})
    else :
        return redirect('autorisation_required', id)

@login_required
def partenaires_edit(request, id, partenaires_id):
    asso = Asso.objects.get(id = id)
    try :
        role = Role.objects.get(asso = asso, user = request.user)
        role = role.role
    except:
        role = 1
    if role > 2:
        partenaire = get_object_or_404(Partenaire, id = partenaires_id)
        edit_form = CreatePartenaire(instance = partenaire)
        delete_form = DeletePartenaire()
        if request.method == 'POST':
            if 'edit_Partenaire' in request.POST:
                edit_form = CreatePartenaire(request.POST, request.FILES, instance = partenaire)
                if edit_form.is_valid():
                    edit_form.save()
                return redirect('partenaires', id)
            if 'Delete_Patenaire' in request.POST:
                delete_form = DeletePartenaire(request.POST)
                if delete_form.is_valid():
                    partenaire.delete()
                    return redirect('partenaires', id)
        context = {
            'asso' : asso,
            'edit_form' : edit_form,
            'delete_form' : delete_form,
            'role' : role,
        }
        return render(request, 'partenaires_edit.html', context)
    else :
        return redirect('autorisation_required', id)


@login_required
def setting_asso(request, id):
    asso = Asso.objects.get(id=id)
    try :
        role = Role.objects.get(asso = asso, user = request.user)
        role = role.role
    except:
        role = 1
    if role > 3 :
        form = SetAsso(instance=asso)
        if request.method == 'POST':
            if 'btn-setasso' in request.POST:
                form = SetAsso(request.POST, request.FILES, instance=asso)
                if form.is_valid():
                    form.save()
                    return redirect('accueil', id)
            elif 'suppasso' in request.POST:
                asso.delete()
                return redirect('index')
            elif 'upgrade_perm' in request.POST:
                promu = User.objects.get(username = request.POST['upgrade_perm'])
                update_role = Role.objects.get(asso=asso, user=promu)
                if update_role.role < 3:
                    update_role.role = 3
                else:
                    update_role.role = 2
                update_role.save()
        # Ajouts de la liste des membres au template pour que le président puisse acorder ou retirer des permissions de niveau 3
        members = asso.user_set.all()
        members_add_btn = []
        #but, obtenir members[[]] avec pour chaque tableau :
            #0 : member
            #1 : message bouton
            #2 : couleur bouton
        for member in members:
            #Problematique si le president change de nom sur son profil ...
            if member.last_name in asso.president:
                pass
            else:
                check_role = Role.objects.get(asso=asso, user=member)
                if check_role.role < 3:
                    add_btn = [member, member.username+" n'a pas le statut d'administrateur, cliquez ici pour lui donner", "3"]
                else:
                    add_btn = [member, "Attention : " + member.username + " est administrateur, cliquez ici pour lui retirer ce statut", "5"]
                members_add_btn.append(add_btn)
        return render(request,'setting_asso.html',{'asso' : asso, 'form' : form, 'role' : role, 'members' : members_add_btn})
    else:
        return redirect('autorisation_required', id)


def autorisation_required(request, id):
    asso = Asso.objects.get(id = id)
    return render(request,'autorisation_required.html',{'asso' : asso})

