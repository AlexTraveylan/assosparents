import requests

def recupasso(RNA_asso):
    """Récupere les données de l'associtation qui correspond au numéro RNA donné.

    Parameters
    ---------
    RNA_asso : str
        RNA de l'association

    Returns
    -------
    array
        0 : code erreur True si reussite. Si False la suite n'existe pas.
        1 : date creation 
        2 : nom
        3 : nom court
        4 : objet
        5 : adresse libelé
        6 : adresse libélé 2
        7 : adresse
        8 : code postal
        9 : ville
        10 : pays

    """
    reponse=[]
    try :
        url=f'https://entreprise.data.gouv.fr/api/rna/v1/id/{RNA_asso}'
        datas=requests.get(url)
        data=datas.json()
        reponse.append(True)
        reponse.append(str(data['association']['date_creation']))
        reponse.append(str(data['association']['titre']))
        reponse.append(str(data['association']['titre_court']))
        reponse.append(str(data['association']['objet']))
        reponse.append(str(data['association']['adresse_gestion_format_postal']))
        reponse.append(str(data['association']['adresse_gestion_geo']))
        reponse.append(str(data['association']['adresse_gestion_libelle_voie']))
        reponse.append(str(data['association']['adresse_gestion_code_postal']))
        reponse.append(str(data['association']['adresse_gestion_acheminement']))
        reponse.append(str(data['association']['adresse_gestion_pays']))
    except :
        reponse.append(False)
    return reponse


# datas=recupasso('W332031955')
# for data in datas:
#     print(data)
