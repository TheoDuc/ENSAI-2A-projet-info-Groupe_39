from business_object.info_manche import InfoManche
from business_object.joueur import Joueur
from dao.manche_joueur_dao import MancheJoueurDAO
from service.credit_service import CreditService
from utils.log_decorator import log


class MancheService:
    """
    Service responsable du déroulement et de la gestion d'une manche de poker :
    - initialisation des joueurs
    - gestion des mises et statuts
    - persistance via la table `manche_joueur`
    """

    dao = MancheJoueurDAO()
    credit_service = CreditService()

    @log
    def initialiser_manche(
        self, id_manche: int, joueurs: list[Joueur], grosse_blind: int
    ) -> InfoManche:
        """
        Initialise une manche :
        - Crée un objet InfoManche avec joueurs, statuts, mises, tours couchés
        - Initialise les crédits temporaires
        - Persiste les participations dans la base (manche_joueur)
        """
        info = InfoManche(joueurs=joueurs)
        info.mises = [0] * len(joueurs)
        info.tour_couche = [0] * len(joueurs)
        info.statuts = ["actif"] * len(joueurs)

        self.credit_service.initialiser_joueurs(joueurs)
        self.dao.creer_manche_joueur(id_manche, info)

        return info

    @log
    def miser(self, id_manche: int, joueur: Joueur, montant: int, info_manche: InfoManche) -> None:
        """
        Débite un joueur de sa mise et met à jour la table manche_joueur.
        """
        if montant <= 0:
            raise ValueError("Le montant misé doit être positif.")

        self.credit_service.debiter(joueur, montant)

        i = info_manche.joueurs.index(joueur)
        info_manche.mises[i] += montant

        self.dao.modifier_manche_joueur(
            id_manche=id_manche,
            id_joueur=joueur.id_joueur,
            mise=info_manche.mises[i],
        )

    @log
    def coucher(self, id_manche: int, joueur: Joueur, info_manche: InfoManche) -> None:
        """
        Met un joueur en statut 'couché' et met à jour la base.
        """
        i = info_manche.joueurs.index(joueur)
        info_manche.statuts[i] = "couché"
        info_manche.tour_couche[i] += 1

        self.dao.modifier_manche_joueur(
            id_manche=id_manche,
            id_joueur=joueur.id_joueur,
            statut="couché",
            tour_couche=info_manche.tour_couche[i],
        )

    @log
    def terminer_manche(
        self, id_manche: int, gagnant: Joueur, info_manche: InfoManche, pot_total: int
    ) -> None:
        """
        Termine la manche :
        - crédite le gagnant
        - finalise les crédits en base
        - met à jour les statuts des joueurs
        """
        self.credit_service.crediter(gagnant, pot_total)

        i = info_manche.joueurs.index(gagnant)
        info_manche.statuts[i] = "gagnant"

        self.dao.modifier_manche_joueur(
            id_manche=id_manche,
            id_joueur=gagnant.id_joueur,
            statut="gagnant",
        )

        self.credit_service.finaliser_credits()

    @log
    def supprimer_manche(self, id_manche: int) -> bool:
        """
        Supprime toutes les participations liées à une manche.
        """
        return self.dao.supprimer_par_id_manche(id_manche)

    @log
    def resume_manche(self, info_manche: InfoManche) -> str:
        """
        Retourne un résumé textuel de la manche.
        """
        lignes = [
            f"{j.pseudo} | Statut: {info_manche.statuts[i]} | Mise: {info_manche.mises[i]} | Tours couchés: {info_manche.tour_couche[i]}"
            for i, j in enumerate(info_manche.joueurs)
        ]
        return "\n".join(lignes)
