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
        """Enregistrement des données en session et mise à jour des joueurs de la table"""
        self.joueur = joueur

        debut = datetime.now(pytz.timezone("Europe/Paris")).strftime("%d/%m/%Y %H:%M:%S")
        self.debut_connexion = debut
        joueur.debut_connexion = debut

        # Ajout du joueur à la liste globale des connectés
        if joueur not in Session.joueurs_connectes:
            Session.joueurs_connectes.append(joueur)

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

        if not self.joueur:
            return res + "Aucun joueur connecté.\n"

        res += f"joueur connecté : {self.joueur.pseudo} : {self.joueur.credit} crédits\n"
        if getattr(self.joueur, "debut_connexion", None):
            res += f"debut_connexion : {self.joueur.debut_connexion}\n"
        res += "\n"

        if self.joueur.table:
            res += f"Joueurs à la table {self.joueur.table.numero_table} :\n"
            res += "-------------------------\n"
            for j in self.joueur.table.joueurs:
                res += f"{j.pseudo} : {j.credit} crédits\n"
            res += "\n"

        return res
