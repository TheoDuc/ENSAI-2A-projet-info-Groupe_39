from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Simple(AbstractCombinaison):
    """Classe représentant une combinaison 'Simple' (la carte la plus haute seule)."""

    def __init__(self, hauteur: str, kicker: tuple[str]):
        """
        Initialise une combinaison Simple.

        Paramètres
        ----------
        hauteur : str
            Valeur de la carte la plus haute.
        kicker : tuple[str]
            Cartes restantes triées par valeur décroissante, servant de kickers pour comparaison.
        """
        super().__init__(hauteur, kicker)

    @classmethod
    def FORCE(cls) -> int:
        """Renvoie la force hiérarchique de la combinaison Simple (0)."""
        return 0

    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        """
        Vérifie si une Simple est présente.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste d’objets Carte à analyser.

        Renvois
        -------
        bool
            True si la liste n’est pas vide (une Simple est toujours présente), False sinon.
        """
        return len(cartes) >= 1

    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "Simple":
        """
        Construit une instance de Simple à partir d’une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste de cartes à partir de laquelle on construit la Simple.

        Renvois
        -------
        Simple
            Instance représentant la carte la plus haute avec ses kickers.

        Exceptions
        ----------
        ValueError
            Si la liste de cartes est vide.
        """

        cls.verifier_min_cartes(cartes)

        cartes_triees = sorted(cartes, key=lambda c: Carte.VALEURS().index(c.valeur), reverse=True)
        hauteur = cartes_triees.pop(0).valeur
        kickers = [c.valeur for c in cartes_triees[:4]]
        return cls(hauteur=hauteur, kicker=kickers)

    def __str__(self) -> str:
        """
        Renvoie une représentation textuelle lisible de la Simple.

        Renvois
        -------
        str
            Exemple : "Simple As et Roi Dame", en incluant les kickers si présents.
        """
        return f"Simple {self.hauteur}"

    def __repr__(self) -> str:
        """
        Renvoie une représentation technique de la Simple

        Renvois
        -------

        """
        return f"Simple(hauteur='{self.hauteur}', kicker={self.kicker})"
