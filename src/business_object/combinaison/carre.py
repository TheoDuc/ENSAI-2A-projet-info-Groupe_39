from collections import Counter
from typing import List

from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Carre(AbstractCombinaison):
    """
    Représente un Carré (quatre cartes de même valeur).

    Un Carré est une combinaison de poker composée de quatre cartes identiques et d'une carte supplémentaire
    appelée "kicker" servant à départager les égalités.
    """

    def __init__(self, hauteur: str, kicker: str) -> None:
        """
        Initialise un objet Carré avec une liste de cartes et un kicker optionnel.

        Paramètres
        ----------
        hauteur : str
            Valeur des cartes formant le Carré (ex. 'Roi').
        kicker : str, optionnel
            Cartes restantes servant à départager les égalités, triées de la plus forte à la plus faible.

        Renvois
        -------
        None

        Exceptions
        ----------
        ValueError
            Levée si le nombre de cartes n’est pas 4 ou si toutes les cartes n’ont pas la même valeur.
        """

        super().__init__(hauteur, kicker)

    @classmethod
    def FORCE(cls) -> int:
        """
        Renvoie la force relative de la combinaison Carré.

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        int
            Force numérique associée au Carré (7).
            Une valeur plus élevée indique une combinaison plus forte.
        """
        return 7

    @classmethod
    def est_present(cls, cartes: List[Carte]) -> bool:
        """
        Vérifie si un Carré est présent dans une liste de cartes.

        Paramètres
        ----------
        cartes : List[Carte]
            Liste des cartes parmi lesquelles rechercher un Carré.

        Renvois
        -------
        bool
            True si une valeur apparaît exactement quatre fois, sinon False.
        """
        valeurs = [c.valeur for c in cartes]
        return any(valeurs.count(v) == 4 for v in set(valeurs))

    @classmethod
    def from_cartes(cls, cartes: List[Carte]) -> "Carre":
        cls.verifier_min_cartes(cartes)

        valeurs = [c.valeur for c in cartes]
        compteur = Counter(valeurs)
        carres_possibles = [v for v, count in compteur.items() if count == 4]

        if not carres_possibles:
            raise ValueError(f"Aucun Carré présent dans les cartes: {dict(compteur)}")

        # Hauteur : string
        hauteur = max(carres_possibles, key=lambda v: Carte.VALEURS().index(v))

        # Kicker : tuple avec une seule carte
        kicker_valeur = max(
            [c.valeur for c in cartes if c.valeur != hauteur],
            key=lambda x: Carte.VALEURS().index(x),
        )

        return cls(hauteur, kicker_valeur)

    def __str__(self) -> str:
        """
        Renvoie une représentation textuelle lisible du Carré.

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        str
            Chaîne lisible par un joueur, par exemple : "Carre de Roi".
        """
        if self.hauteur == "As":
            return "Carre d'As"
        return f"Carre de {self.hauteur}"

    def __repr__(self) -> str:
        """
        Renvoie une représentation technique du Carré
        Paramètres
        ----------
        Aucun

        Renvois
        -------
        str
            Chaîne détaillant la combinaison, par exemple :
            "Carre([Roi de Coeur, Roi de Pique, Roi de Carreau, Roi de Trèfle])".
        """

        return f"Carre(hauteur={self.hauteur}, kicker={self.kicker})"
