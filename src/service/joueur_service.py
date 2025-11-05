import logging

from business_object.joueur import Joueur
from dao.joueur_dao import JoueurDao
from utils.log_decorator import log

logger = logging.getLogger(__name__)


class JoueurService:
    """
    Service pour gérer les joueurs :
    - CRUD (création, lecture, modification, suppression)
    - Rattachement à une table
    - Gestion des crédits via les méthodes de Joueur
    """

    # dao = JoueurDao()

    def __init__(self, dao=None):
        # On peut injecter un mock DAO pour les tests
        self.dao = dao or JoueurDao()

    @log
    def se_connecter(self, pseudo: str) -> Joueur | None:
        """Simule la connexion d’un joueur via son pseudo"""
        return self.dao.se_connecter(pseudo)

    @log
    def pseudo_deja_utilise(self, pseudo: str) -> bool:
        """
        Vérifie si un pseudo existe déjà dans la base

        Paramètres
        ----------
        pseudo : str
            Pseudo à vérifier

        Renvois
        -------
        bool
            True si le pseudo existe, False sinon
        """
        return self.dao.se_connecter(pseudo) is not None

    @log
    def creer(self, pseudo: str, pays: str) -> Joueur | None:
        """Crée un joueur avec 2000 crédits par défaut si le pseudo n’existe pas déjà"""
        if self.pseudo_deja_utilise(pseudo):  # vérifie si le pseudo existe
            logger.warning(f"Pseudo {pseudo} déjà utilisé")
            return None

        nouveau_joueur = Joueur(
            id_joueur=1,  # L'ID réel peut être géré par le DAO
            pseudo=pseudo,
            credit=2000,
            pays=pays,
        )
        return nouveau_joueur if self.dao.creer(nouveau_joueur) else None

    @log
    def trouver_par_id(self, id_joueur: int) -> Joueur | None:
        """Récupère un joueur par ID"""
        return self.dao.trouver_par_id(id_joueur)

    @log
    def lister_tous(self) -> list[Joueur]:
        """Liste tous les joueurs"""
        return self.dao.lister_tous()

    @log
    def modifier(self, joueur: Joueur) -> Joueur | None:
        """Met à jour les informations d’un joueur via DAO"""
        return joueur if self.dao.modifier(joueur) else None

    @log
    def supprimer(self, joueur: Joueur) -> bool:
        """Supprime un joueur via DAO"""
        return self.dao.supprimer(joueur)
