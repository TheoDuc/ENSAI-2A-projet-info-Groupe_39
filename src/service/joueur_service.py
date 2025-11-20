import logging

from business_object.joueur import Joueur
from dao.joueur_dao import JoueurDao
from utils.log_decorator import log

logger = logging.getLogger(__name__)


class JoueurService:
    """
    Service pour la gestion des joueurs :
    - CRUD (création, lecture, modification, suppression)
    - Rattachement à une table
    - Gestion des crédits via les méthodes de Joueur
    """
    def __init__(self):
        self.dao = JoueurDao()
        self._joueurs_connectes: dict[int, Joueur] = {}

    @log
    def se_connecter(self, pseudo: str) -> Joueur | None:
        """Simule la connexion d’un joueur via son pseudo"""
        joueur = self.dao.se_connecter(pseudo)

        if joueur.id_joueur in self._joueurs_connectes.keys():
            raise Exception(f"Le joueur {joueur.pseudo} est déjà connecté !")

        if joueur:
            self._joueurs_connectes[joueur.id_joueur] = joueur
        return self._joueurs_connectes[joueur.id_joueur]

    @log
    def deconnexion(self, id_joueur: int) -> None:
        """Déconnecte un joueur de l'application"""
        if id_joueur not in self._joueurs_connectes:
            raise Exception(f"Le joueur avec l'identifiant {id_joueur} n'est pas connecté.")

        del self._joueurs_connectes[id_joueur]

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

        try:
            created = self.dao.creer(pseudo, pays)
            if created:
                joueur = self.dao.se_connecter(pseudo)
                logger.info(f"Joueur créé avec succès : {joueur}")
                return joueur
        except Exception as e:
            logger.error(f"Erreur lors de la création du joueur {pseudo} : {e}")

        return None

    def trouver_par_id(self, id_joueur: int) -> Joueur | None:
        """Récupère un joueur par ID"""
        if id_joueur in self._joueurs_connectes.keys():
            return self._joueurs_connectes[id_joueur]
        
        raise ValueError(f"Le joueur avec l'identifiant {id_joueur} n'est pas connecté")

    def trouver_par_pseudo(self, pseudo: str) -> Joueur | None:
        """Récupère un joueur par pseudo"""
        return self.dao.trouver_par_pseudo(pseudo)

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
