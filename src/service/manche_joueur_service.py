from logs.logger import log

from business_object.joueur import Joueur
from dao.manche_joueur_dao import MancheJoueurDAO


class MancheJoueurService:
    dao = MancheJoueurDAO()

    @log
    def trouver_par_ids(self, id_manche: int, id_joueur: int) -> list[dict]:
        """Récupère les participations d’un joueur spécifique à une manche."""
        return self.dao.trouver_par_ids(id_manche, id_joueur)

    @log
    def creer_manche_joueur(self, id_manche: int, info_manche) -> bool:
        """Crée les participations des joueurs à une manche."""
        return self.dao.creer_manche_joueur(id_manche, info_manche)

    @log
    def trouver_joueur_par_manche(self, id_manche: int, id_joueur: int) -> dict | None:
        participations = self.trouver_par_ids(id_manche, id_joueur)
        return participations[0] if participations else None

    @log
    def supprimer_par_id_manche(self, id_manche: int) -> bool:
        """Supprime toutes les participations liées à une manche."""
        return self.dao.supprimer_par_id_manche(id_manche)

    @log
    def ajouter_joueur(self, manche_id: int, joueur: Joueur) -> bool:
        """Ajoute un joueur à une manche"""
        return self.dao.ajouter_joueur_a_manche(manche_id, joueur.id_joueur)

    @log
    def retirer_joueur(self, manche_id: int, joueur_id: int) -> bool:
        """Retire un joueur d’une manche"""
        return self.dao.retirer_joueur_de_manche(manche_id, joueur_id)

    @log
    def lister_joueurs(self, manche_id: int) -> list[Joueur]:
        """Récupère la liste des joueurs d’une manche avec leurs informations"""
        joueurs_data = self.dao.trouver_joueurs_par_manche(manche_id)
        return [Joueur(**data) for data in joueurs_data]

    @log
    def obtenir_info_joueur(self, manche_id: int, joueur_id: int) -> Joueur | None:
        """Récupère les informations d’un joueur spécifique pour une manche"""
        res = self.dao.trouver_joueur_par_manche(manche_id, joueur_id)
        return Joueur(**res) if res else None
