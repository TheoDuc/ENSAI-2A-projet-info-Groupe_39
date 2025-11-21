import os
from datetime import datetime

import pytz
import requests

from business_object.joueur import Joueur
from business_object.table import Table
from service.joueur_service import JoueurService
from utils.singleton import Singleton

host = os.environ.get("HOST_WEBSERVICE")


class Session(metaclass=Singleton):
    """Stocke les données de session et gère les joueurs connectés et les tables."""

    joueurs_connectes = []
    tables_globales = {}

    def __init__(self):
        self.id = None
        self.debut_connexion = None

    def connexion(self, joueur: Joueur):
        self.id = joueur.id_joueur
        self.debut_connexion = datetime.now(pytz.timezone("Europe/Paris")).strftime(
            "%d/%m/%Y %H:%M:%S"
        )
        joueur.debut_connexion = self.debut_connexion

        if joueur not in Session.joueurs_connectes:
            Session.joueurs_connectes.append(joueur)

        # Mettre à jour la table globale si le joueur est dans une table
        if joueur.numero_table is not None:
            table = Session.tables_globales.get(joueur.numero_table)
            if table:
                for id_j in table.id_joueurs:
                    j = JoueurService().trouver_par_id(id_j)
                    if j not in Session.joueurs_connectes:
                        Session.joueurs_connectes.append(j)

    def deconnexion(self):
        self.id = None
        self.debut_connexion = None

    def refresh(self):
        """Rafraîchit les informations du joueur et des tables depuis l'API."""
        if not self.id:
            return

        # Récupérer le joueur depuis l'API
        try:
            res = requests.get(f"{host}/joueur/id/{self.id}").json()
        except Exception:
            return

        joueur = JoueurService().trouver_par_id(self.id)
        joueur.numero_table = res.get("_Joueur__numero_table")

        # Rafraîchir la table globale si nécessaire
        if joueur.numero_table:
            try:
                table_res = requests.get(f"{host}/table/{joueur.numero_table}")
                if table_res.status_code == 200:
                    table_json = table_res.json()
                    Session.tables_globales[joueur.numero_table] = Table.from_json(table_json)
            except Exception:
                pass

    def afficher(self) -> str:
        self.refresh()
        res = "Actuellement en session :\n" + "-" * 25 + "\n"
        if not self.id:
            return res + "Aucun joueur connecté.\n"
        joueur = JoueurService().trouver_par_id(self.id)
        res += f"Joueur connecté : {joueur.pseudo} : {joueur.credit} crédits\n"
        if getattr(joueur, "debut_connexion", None):
            res += f"Début connexion : {joueur.debut_connexion}\n"

        if joueur.numero_table:
            table = Session.tables_globales.get(joueur.numero_table)
            if table:
                res += f"\nJoueurs à la table {table.numero_table} :\n" + "-" * 40 + "\n"
                for id_j in table.id_joueurs:
                    j = JoueurService().trouver_par_id(id_j)
                    debut = getattr(j, "debut_connexion", "Non connecté")
                    res += f"{j.pseudo} : {j.credit} crédits (connexion : {debut})\n"
        return res
