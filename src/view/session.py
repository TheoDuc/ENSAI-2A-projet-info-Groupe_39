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
        """Afficher le joueur connecté et tous les joueurs à sa table"""
        res = "Actuellement en session :\n"
        res += "-------------------------\n"

        joueur = self.joueur
        if not joueur:
            return res + "Aucun joueur connecté.\n"

        res += f"joueur connecté : {joueur.pseudo} : {joueur.credit} crédits\n"
        if getattr(joueur, "debut_connexion", None):
            res += f"debut_connexion : {joueur.debut_connexion}\n"
        res += "\n"

        # Vérifie si le joueur est dans une table
        if joueur.table:
            res += f"Joueurs à la table {joueur.table.numero_table} :\n"
            res += "-------------------------\n"
            for j in joueur.table.joueurs:
                res += f"{j.pseudo} : {j.credit} crédits\n"
            res += "\n"

        return res
