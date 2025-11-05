from logs.logger import log

from business_object.joueur import Joueur
from dao.manche_joueur_dao import MancheJoueurDAO


class MancheJoueurService:
    dao = MancheJoueurDAO()

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
