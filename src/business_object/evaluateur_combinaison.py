from typing import List
from business_object.carte import Carte
from business_object.combinaison.combinaison import (
    AbstractCombinaison,
    QuinteFlush,
    Carre,
    Full,
    Couleur,
    Quinte,
    Brelan,
    DoublePaire,
    Paire,
    Simple,
)


class EvaluateurCombinaison:
    """
    Classe utilitaire pour évaluer la meilleure combinaison de poker
    à partir d'une main donnée.
    
    Attributs
    ---------
    COMBINAISONS : list
        Liste ordonnée des classes de combinaisons, de la plus forte
        à la plus faible. L'ordre est crucial pour l'évaluation.
    """

    COMBINAISONS = [
        QuinteFlush,  # La combinaison la plus forte
        Carre,        # Quatre cartes identiques
        Full,         # Trois cartes identiques + une paire
        Couleur,      # 5 cartes de la même couleur
        Quinte,       # 5 cartes consécutives
        Brelan,       # Trois cartes identiques
        DoublePaire,  # Deux paires
        Paire,        # Une paire
        Simple,       # Carte haute (aucune combinaison)
    ]

    @staticmethod
    def eval(cartes: List[Carte]) -> AbstractCombinaison:
        """
        Évalue la meilleure combinaison présente dans une liste de cartes.

        Paramètres
        ----------
        cartes : List[Carte]
            Liste de cartes représentant la main ou les cartes disponibles.

        Retourne
        -------
        AbstractCombinaison
            Instance de la sous-classe correspondant à la combinaison détectée.

        Exceptions
        ----------
        ValueError
            Si la liste de cartes contient moins de 5 cartes.

        Exemple
        -------
        >>> cartes = [Carte('C', '10'), Carte('C', 'J'), Carte('C', 'Q'), Carte('C', 'K'), Carte('C', 'A')]
        >>> combinaison = EvaluateurCombinaison.eval(cartes)
        >>> isinstance(combinaison, QuinteFlush)
        True
        """
        if not cartes or len(cartes) < 5:
            raise ValueError(
                f"Au moins 5 cartes sont nécessaires pour évaluer une combinaison, "
                f"actuellement {len(cartes)}."
            )

        # Parcours des combinaisons de la plus forte à la plus faible
        for C in EvaluateurCombinaison.COMBINAISONS:
            if C.est_present(cartes):
                return C.from_cartes(cartes)

        # Cas théorique : aucune combinaison ne correspond
        # Renvoie simplement la carte la plus haute
        return Simple.from_cartes(cartes)
