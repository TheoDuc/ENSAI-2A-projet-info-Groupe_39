"""Service métier pour la gestion des joueurs (Poker)."""

from business_object.joueur import Joueur
from dao.joueur_dao import JoueurDao
from utils.log_decorator import log


class JoueurService:
    """
    Service contenant les opérations principales liées aux joueurs :
    - création, recherche, modification et suppression ;
    - gestion du rattachement à une table ;
    - consultation des informations de base.
    """

    def __init__(self):
        self.dao = JoueurDao()

    # --- CRUD de base ---

    @log
    def creer(self, pseudo: str, credit: int, pays: str) -> Joueur:
        """
        Crée un joueur et l’enregistre dans la base de données.

        Paramètres
        ----------
        pseudo : str
            Nom du joueur
        credit : int
            Crédits initiaux
        pays : str
            Pays du joueur

        Renvoie
        -------
        Joueur | None
            Le joueur créé, ou None si échec de création.
        """

        nouveau_joueur = Joueur(
            id_joueur=1,
            pseudo=pseudo,
            credit=credit,
            pays=pays,
        )

        return nouveau_joueur if self.dao.creer(nouveau_joueur) else None

    @log
    def trouver_par_id(self, id_joueur: int) -> Joueur:
        """Recherche un joueur dans la base de donnée par son identifiant."""
        return self.dao.trouver_par_id(id_joueur)

    @log
    def lister_tous(self) -> list[Joueur]:
        """Retourne la liste de tous les joueurs enregistrés dans la base."""
        return self.dao.lister_tous()

    @log
    def modifier(self, joueur: Joueur) -> Joueur:
        """
        Met à jour les informations d’un joueur en base.
        Retourne le joueur modifié si la mise à jour réussit.
        """
        return joueur if self.dao.modifier(joueur) else None

    @log
    def supprimer(self, joueur: Joueur) -> bool:
        """Supprime un joueur de la base de données."""
        return self.dao.supprimer(joueur)
