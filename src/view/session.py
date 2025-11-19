from datetime import datetime

import pytz

from utils.singleton import Singleton


class Session(metaclass=Singleton):
    """Stocke les données liées à une session.
    Cela permet par exemple de connaitre le joueur connecté à tout moment
    depuis n'importe quelle classe.
    Sans cela, il faudrait transmettre ce joueur entre les différentes vues.
    """

    joueurs_connectes = []

    def __init__(self):
        """Création de la session"""
        self.joueur = None
        self.debut_connexion = None

    def connexion(self, joueur):
        """Enregistement des données en session"""
        self.joueur = joueur
        debut = datetime.now(pytz.timezone("Europe/Paris")).strftime("%d/%m/%Y %H:%M:%S")
        self.debut_connexion = debut
        joueur.debut_connexion = debut
        if joueur not in Session.joueurs_connectes:
            Session.joueurs_connectes.append(joueur)
        if joueur.table:
            for j in joueur.table.joueurs:
                if j not in Session.joueurs_connectes:
                    Session.joueurs_connectes.append(j)

    def deconnexion(self):
        if self.joueur in Session.joueurs_connectes:
            Session.joueurs_connectes.remove(self.joueur)
        """Suppression des données de la session"""
        self.joueur = None
        self.debut_connexion = None

    def afficher(self) -> str:
        """Afficher tous les joueurs connectés et ceux présents aux tables"""
        res = "Actuellement en session :\n"
        res += "-------------------------\n"

        # Joueurs connectés globalement
        for j in Session.joueurs_connectes:
            res += f"joueur connecté : {j.pseudo} : {j.credit} crédits\n"
            if getattr(j, "debut_connexion", None):
                res += f"debut_connexion : {j.debut_connexion}\n"
            res += "\n"

        # Joueurs par table
        tables_affichees = set()
        for j in Session.joueurs_connectes:
            if j.table and j.table not in tables_affichees:
                tables_affichees.add(j.table)
                res += f"Table {j.table.numero_table} :\n"
                res += "-------------------------\n"
                for joueur_table in j.table.joueurs:
                    res += f"{joueur_table.pseudo} : {joueur_table.credit} crédits\n"
                res += "\n"

        return res
