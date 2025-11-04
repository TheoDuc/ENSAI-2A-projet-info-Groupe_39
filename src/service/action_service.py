"""Implémentation de la classe ActionService"""

from business_object.joueur import Joueur
from business_object.manche import Manche
from service.credit_service import CreditService


class ActionService:
    """Modélisation des actions possibles d'un joueur dans une Manche"""

    def manche_joueur(self, joueur: Joueur) -> Manche:
        """Blabla"""

        if joueur.table is None:
            raise ValueError(
                f"Le joueur {joueur.pseudo} n'est à aucune table et ne peut effectuer d'action"
            )

        if joueur.table.manche is None:
            raise ValueError(
                f"Le joueur {joueur.pseudo} est dans une table mais aucune manche n'est en cours"
            )

        if joueur not in joueur.table.manche.info.joueurs:
            raise ValueError(f"Le joueur {joueur.pseudo} ne participe pas à la manche en cours")

        return joueur.table.manche

    def all_in(self, joueur: Joueur) -> bool:
        """Blabla"""

        manche = self.manche_joueur(joueur)
        indice_joueur = manche.indice_joueur(joueur)

        if not manche.est_tour(joueur):
            raise Exception(f"Ce n'est pas à {joueur.pseudo} de jouer")

        montant = manche.info.all_in(indice_joueur)
        CreditService().debiter(joueur, montant)
        return True

    def checker(self, joueur: Joueur) -> bool:
        """Blabla"""

        manche = self.manche_joueur(joueur)
        indice_joueur = manche.indice_joueur(joueur)

        if not manche.est_tour(joueur):
            raise Exception(f"Ce n'est pas à {joueur.pseudo} de jouer")

        if not manche.info.statuts[indice_joueur] == 2:
            print(f"{joueur.pseudo} ne peut pas checker car il est en retard sur les mises")
            return False

        manche.info.mettre_statut(indice_joueur, 2)
        return True

    def se_coucher(self, joueur: Joueur) -> bool:
        """Blabla"""

        manche = self.manche_joueur(joueur)
        indice_joueur = manche.indice_joueur(joueur)

        if not manche.est_tour(joueur):
            raise Exception(f"Ce n'est pas à {joueur.pseudo} de jouer")

        manche.info.coucher_joueur(indice_joueur, 3)
        return True

    def suivre(self, joueur: Joueur, relance: int = 0) -> bool:
        """Blabla"""

        manche = self.manche_joueur(joueur)
        indice_joueur = manche.indice_joueur(joueur)

        if not manche.est_tour(joueur):
            raise Exception(f"Ce n'est pas à {joueur.pseudo} de jouer")

        montant = manche.info.suivre(indice_joueur, relance)
        CreditService().debiter(joueur, montant)
        return True
