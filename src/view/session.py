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
        self.debut_connexion = datetime.now(pytz.timezone("Europe/Paris")).strftime(
            "%d/%m/%Y %H:%M:%S"
        )
        if joueur not in Session.joueurs_connectes:
            Session.joueurs_connectes.append(joueur)

    def deconnexion(self):
        if self.joueur in Session.joueurs_connectes:
            Session.joueurs_connectes.remove(self.joueur)
        """Suppression des données de la session"""
        self.joueur = None
        self.debut_connexion = None

    def afficher(self) -> str:
        """Afficher les informations de connexion"""
        res = "Actuellement en session :\n"
        res += "-------------------------\n"
        for j in Session.joueurs_connectes:
            res += f"joueur : {j.pseudo} : {j.credit} crédits\n"
            debut = getattr(j, "debut_connexion", None)
            if debut:
                res += f"debut_connexion : {debut}\n"
            res += "\n"
        return res
