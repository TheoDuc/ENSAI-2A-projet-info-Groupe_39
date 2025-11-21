import os
from datetime import datetime

import pytz
import requests

from business_object.joueur import Joueur
from service.joueur_service import JoueurService
from utils.singleton import Singleton


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

        if joueur.numero_table is not None:
            table = Session.tables_globales.get(joueur.numero_table)
            for id_j in table.id_joueurs:
                js = JoueurService().trouver_par_id(id_j)
                if js not in Session.joueurs_connectes:
                    Session.joueurs_connectes.append(js)

    def deconnexion(self):
        """Suppression des données de la session"""
        self.id = None
        self.debut_connexion = None

    def afficher(self) -> str:
        res = "Actuellement en session :\n" + "-" * 25 + "\n"

        if self.id is None:
            return res + "Aucun joueur connecté.\n"

        host = os.environ.get("HOST_WEBSERVICE")
        url = f"{host}/joueur/id/{self.id}"

        try:
            reponse = requests.get(url).json()
        except Exception:
            return res + "Erreur : impossible de récupérer le joueur.\n"

        if not reponse or "_Joueur__id_joueur" not in reponse:
            return res + "Aucun joueur connecté.\n"

        # Instanciation du joueur depuis la réponse JSON
        joueur = Joueur(
            id_joueur=reponse["_Joueur__id_joueur"],
            pseudo=reponse["_Joueur__pseudo"],
            credit=reponse["_Joueur__credit"],
            pays=reponse["_Joueur__pays"],
            numero_table=reponse.get("_Joueur__numero_table"),
        )

        # Ajout du joueur à la liste globale si absent
        if joueur not in Session.joueurs_connectes:
            Session.joueurs_connectes.append(joueur)

        res += f"Joueur connecté : {joueur.pseudo} : {joueur.credit} crédits\n"
        if getattr(joueur, "debut_connexion", None):
            res += f"Début connexion : {joueur.debut_connexion}\n"

        # Affichage des joueurs à la même table
        if joueur.table:
            numero_table = joueur.numero_table
            res += f"\nJoueurs à la table {numero_table} :\n" + "-" * 40 + "\n"
            for id_j in joueur.table.id_joueurs:
                j = JoueurService().trouver_par_id(id_j)
                debut = getattr(j, "debut_connexion", "Non connecté")
                res += f"{j.pseudo} : {j.credit} crédits (connexion : {debut})\n"

        return res
