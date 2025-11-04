from typing import List

from business_object.carte import Carte
from business_object.combinaison.brelan import Brelan
from business_object.combinaison.carre import Carre
from business_object.combinaison.combinaison import AbstractCombinaison
from business_object.combinaison.couleur import Couleur
from business_object.combinaison.double_paire import DoublePaire
from business_object.combinaison.full import Full
from business_object.combinaison.paire import Paire
from business_object.combinaison.quinte import Quinte
from business_object.combinaison.quinte_flush import QuinteFlush
from business_object.combinaison.simple import Simple

class EvaluateurCombinaison:
    """
    Évalue la meilleure combinaison d'une main de poker donnée.
    (Ne compare pas plusieurs mains, juste l'identification.)
    """

    COMBINAISONS = [
        QuinteFlush,
        Carre,
        Full,
        Couleur,
        Quinte,
        Brelan,
        DoublePaire,
        Paire,
        Simple,
    ]

    @staticmethod
    def eval(cartes: List[Carte]) -> AbstractCombinaison:
        """
        Détermine la combinaison présente dans la liste de cartes.

        Retourne une instance de la bonne sous-classe de AbstractCombinaison.
        """
        if not cartes or len(cartes) < 5:
            raise ValueError(f"Au moins 5 cartes sont nécessaires, actuellement {len(cartes)}")

        for C in EvaluateurCombinaison.COMBINAISONS:
            if C.est_present(cartes):
                return C.from_cartes(cartes)

        # Si aucune combinaison ne correspond (cas théorique)
        return Simple.from_cartes(cartes)
