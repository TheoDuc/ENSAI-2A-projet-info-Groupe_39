from collections import Counter
from typing import List

from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Full(AbstractCombinaison):
    """Classe représentant un Full (Brelan + Paire) au poker."""

    def __init__(self, hauteur: list[str], kicker=None) -> None:
        """
        Initialise une combinaison Full.

        Paramètres
        ----------
        hauteur : list[str]
            Liste de deux valeurs : [brelan, paire], la plus forte en premier.

        Renvois
        -------
        None
        """
        # hauteur = sorted(hauteur, key=lambda x: Carte.VALEURS().index(x), reverse=True)
        super().__init__(hauteur, kicker)

    @classmethod
    def FORCE(cls) -> int:
        """
        Renvoie la force hiérarchique de la combinaison Full.

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        int
            Valeur entière correspondant à la force du Full (6).
        """
        return 6

    @classmethod
    def est_present(cls, cartes: List["Carte"]) -> bool:
        """
        Vérifie si un Full est présent dans une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste d’objets Carte à analyser.

        Renvois
        -------
        bool
            True si un Brelan et une Paire distincte sont présents, False sinon.
        """
        valeurs = [c.valeur for c in cartes]
        compteur = Counter(valeurs)
        has_brelan = any(count >= 3 for count in compteur.values())
        has_paire = any(count >= 2 for v, count in compteur.items() if count < 3)
        return has_brelan and has_paire

    @classmethod
    def from_cartes(cls, cartes: List["Carte"]) -> "Full":
        """
        Construit une instance de Full à partir d’une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste de cartes à partir de laquelle on cherche un Full.

        Renvois
        -------
        Full
            Instance représentant le Full détecté.

        Exceptions
        ----------
        ValueError
            Si aucun Brelan ou Paire n’est trouvé pour constituer le Full.
        """
        cls.verifier_min_cartes(cartes)
        valeurs = [c.valeur for c in cartes]
        compteur = Counter(valeurs)

        # Le brelan le plus fort
        brelans = [v for v, count in compteur.items() if count >= 3]
        if not brelans:
            raise ValueError("Aucun brelan pour former un Full")
        brelan = max(brelans, key=lambda v: Carte.VALEURS().index(v))

        # La paire la plus forte différente du brelan
        paires = [v for v, count in compteur.items() if count >= 2 and v != brelan]
        if not paires:
            raise ValueError("Aucune paire pour former un Full")
        paire = max(paires, key=lambda v: Carte.VALEURS().index(v))

        return cls(hauteur=[brelan, paire])

    def __str__(self) -> str:
        """
        Renvoie une représentation lisible du Full pour le joueur.

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        str
            Exemple : "Full Dame Roi".
        """
        return f"Full {self.hauteur[0]} {self.hauteur[1]}"

    def __repr__(self) -> str:
        """
        Renvoie une représentation technique du Full pour le débogage.

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        str
            Exemple : "Full(Hauteur(Dame), Paire(Roi))".
        """
        return f"Full(hauteur={self.hauteur}, kicker={self.kicker})"
