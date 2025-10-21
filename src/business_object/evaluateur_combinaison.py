from typing import List

from business_object.carte import Carte
from business_object.combinaison.brelan import Brelan
from business_object.combinaison.carre import Carre
from business_object.combinaison.couleur import Couleur
from business_object.combinaison.double_paire import DoublePaire
from business_object.combinaison.full import Full
from business_object.combinaison.paire import Paire
from business_object.combinaison.quinte import Quinte
from business_object.combinaison.quinte_flush import QuinteFlush
from business_object.combinaison.simple import Simple


class EvaluateurCombinaison:
    """
    Classe pour évaluer la meilleure combinaison de 5 cartes.
    """

    @staticmethod
    def eval(cartes: List[Carte]):
        """
        Évalue la meilleure combinaison parmi les cartes fournies.
        Retourne une instance de la classe correspondante.
        """
        if not cartes or len(cartes) < 5:
            raise ValueError(
                f"Au moins 5 cartes sont nécessaires pour évaluer une combinaison : {cartes}"
            )

        # Priorité des combinaisons par force décroissante
        try:
            if QuinteFlush.est_present(cartes):
                return QuinteFlush.from_cartes(cartes)
            if Carre.est_present(cartes):
                return Carre.from_cartes(cartes)
            if Full.est_present(cartes):
                return Full.from_cartes(cartes)
            if Couleur.est_present(cartes):
                return Couleur.from_cartes(cartes)
            if Quinte.est_present(cartes):
                return Quinte.from_cartes(cartes)
            if Brelan.est_present(cartes):
                return Brelan.from_cartes(cartes)
            if DoublePaire.est_present(cartes):
                return DoublePaire.from_cartes(cartes)
            if Paire.est_present(cartes):
                return Paire.from_cartes(cartes)
            return Simple.from_cartes(cartes)
        except Exception as e:
            # On enrichit le message avec la valeur problématique
            raise ValueError(
                f"Erreur lors de l'évaluation de la combinaison pour les cartes {cartes}: {e}"
            ) from e
