from datetime import datetime

import os
import requests
import pytz

from utils.singleton import Singleton
from service.joueur_service import JoueurService
from business_object.joueur import Joueur


class Session(metaclass=Singleton):
    """Stocke les données liées à une session.
    Cela permet par exemple de connaitre le joueur connecté à tout moment
    depuis n'importe quelle classe.
    Sans cela, il faudrait transmettre ce joueur entre les différentes vues.
    """

    joueurs_connectes = []
    tables_globales = {}

    def __init__(self):
        """Création de la session"""
        self.id = None
        self.debut_connexion = None

    def connexion(self, joueur):
        """Enregistrement des données en session et mise à jour des joueurs de la table"""
        self.id = joueur.id_joueur

        debut = datetime.now(pytz.timezone("Europe/Paris")).strftime("%d/%m/%Y %H:%M:%S")
        self.debut_connexion = debut
        joueur.debut_connexion = debut

        # Ajout du joueur à la liste globale des connectés
        if joueur not in Session.joueurs_connectes:
            Session.joueurs_connectes.append(joueur)

        if joueur.table:
            for j in joueur.table.joueurs:
                if j not in Session.joueurs_connectes:
                    Session.joueurs_connectes.append(j)

    def deconnexion(self):
        """Suppression des données de la session"""
        self.id = None
        self.debut_connexion = None

    def afficher(self) -> str:
        res = "Actuellement en session :\n"
        res += "-------------------------\n"

        host = os.environ["HOST_WEBSERVICE"]
        END_POINT = "/joueur/id"

        url = f"{host}{END_POINT}/{self.id}"
        req = requests.get(url)
        
        reponse = req.json()
        joueur = Joueur(
            id_joueur=reponse["_Joueur__id_joueur"],
            pseudo=reponse["_Joueur__pseudo"],
            credit=reponse["_Joueur__credit"],
            pays=reponse["_Joueur__pays"],
        )

        if not joueur:
            return res + "Aucun joueur connecté.\n"

        res += f"Joueur connecté : {joueur.pseudo} : {joueur.credit} crédits\n"
        if getattr(joueur, "debut_connexion", None):
            res += f"Début connexion : {joueur.debut_connexion}\n"
        res += "\n"

        print(
            f"[DEBUG] Joueur {joueur.pseudo} est sur la table : {getattr(joueur.table, 'numero_table', 'Aucune')}"
        )

        # Tous les joueurs à la même table
        if joueur.table:
            numero_table = joueur.table.numero_table
            res += f"Joueurs à la table {numero_table} :\n"
            res += "-" * 40 + "\n"

            # Récupération des joueurs depuis la table globale
            table = Session.tables_globales.get(numero_table)
            print(table)
            if table:
                for j in table.joueurs:
                    # On cherche le joueur dans la liste globale des connectés
                    if j in Session.joueurs_connectes:
                        debut = getattr(j, "debut_connexion", "Connexion inconnue")
                    else:
                        debut = "Non connecté"
                    res += f"{j.pseudo} : {j.credit} crédits (connexion : {debut})\n"
            else:
                res += "Impossible de récupérer les joueurs de la table.\n"

        return res
