from business_object.joueur import Joueur
from dao.joueur_dao import JoueurDao
from utils.log_decorator import log


class JoueurService:
    """
    Service métier pour la gestion des joueurs :
    - CRUD (création, lecture, modification, suppression)
    - Gestion du rattachement à une table
    - Consultation des informations d’un joueur
    """

    dao = JoueurDao()

    # --- CRUD de base ---

    @log
    def creer(self, pseudo: str, credit: int, pays: str) -> Joueur | None:
        """
        Crée un joueur et l’enregistre via le DAO.
        """
        # Génération d'un id temporaire, réel id géré par le DAO
        nouveau_joueur = Joueur(
            id_joueur=0,
            pseudo=pseudo,
            credit=credit,
            pays=pays,
        )
        return nouveau_joueur if self.dao.creer(nouveau_joueur) else None

    @log
    def trouver_par_id(self, id_joueur: int) -> Joueur | None:
        """
        Recherche un joueur dans la base par son identifiant.
        """
        return self.dao.trouver_par_id(id_joueur)

    @log
    def lister_tous(self) -> list[Joueur]:
        """
        Retourne tous les joueurs enregistrés.
        """
        return self.dao.lister_tous()

    @log
    def modifier(self, joueur: Joueur) -> Joueur | None:
        """
        Met à jour un joueur via le DAO.
        """
        return joueur if self.dao.modifier(joueur) else None

    @log
    def supprimer(self, joueur: Joueur) -> bool:
        """
        Supprime un joueur via le DAO.
        """
        return self.dao.supprimer(joueur)
