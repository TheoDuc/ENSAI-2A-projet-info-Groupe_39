from typing import List, Tuple

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
    Évalue la meilleure combinaison de poker dans une liste de cartes
    et calcule un score numérique pour la comparer facilement.
    """

    @staticmethod
    def eval(cartes: List[Carte]) -> AbstractCombinaison:
        """
        Détermine la meilleure combinaison possible dans une liste de cartes.
        """
        if not cartes or len(cartes) < 5:
            raise ValueError(f"Au moins 5 cartes sont nécessaires, actuellement {len(cartes)}")

        # Liste des combinaisons à tester par ordre de force
        combinaisons = [
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

        for C in combinaisons:
            if C.est_present(cartes):
                return C.from_cartes(cartes)

        # Fallback (Simple)
        return Simple.from_cartes(cartes)

    @staticmethod
    def score(combi: AbstractCombinaison) -> int:
        """
        Transforme une combinaison en score unique pour comparer deux mains.
        """
        score = combi.FORCE() * 10**10  # Priorité de la combinaison

        # Hauteur principale
        hauteurs = combi.hauteur if isinstance(combi.hauteur, list) else [combi.hauteur]
        for i, h in enumerate(hauteurs):
            score += (14 - Carte.VALEURS().index(h)) * 10 ** (8 - i * 2)

        # Kicker(s)
        if combi.kicker:
            kickers = combi.kicker if isinstance(combi.kicker, list) else [combi.kicker]
            for i, k in enumerate(kickers):
                v = k.valeur if isinstance(k, Carte) else k
                score += (14 - Carte.VALEURS().index(v)) * 10 ** (6 - i * 2)

        return score

    @staticmethod
    def meilleure_main(cartes: List[Carte]) -> Tuple[AbstractCombinaison, int]:
        """
        Retourne la meilleure combinaison et son score pour comparaison rapide.
        """
        combi = EvaluateurCombinaison.eval(cartes)
        return combi, EvaluateurCombinaison.score(combi)
