from collections import Counter

from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Paire(AbstractCombinaison):
    """Classe représentant une Paire (deux cartes de même valeur) au poker."""

    def __init__(self, hauteur: str, kicker: tuple[str]) -> None:
        """
        Initialise une combinaison Paire.

        Paramètres
        ----------
        hauteur : str
            Valeur de la Paire.
        kicker : tuple[str]
            Cartes restantes servant de kickers pour comparaison.
        """
        super().__init__(hauteur, kicker)

    @classmethod
    def FORCE(cls) -> int:
        """Renvoie la force hiérarchique de la combinaison Paire (1)."""
        return 1

    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        """
        Vérifie si une Paire est présente dans une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste d’objets Carte à analyser.

        Renvois
        -------
        bool
            True si au moins une Paire est présente, False sinon.
        """
        valeurs = [c.valeur for c in cartes]
        compteur = Counter(valeurs)
        return any(count >= 2 for count in compteur.values())

    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "Paire":
        """
        Construit une instance de Paire à partir d’une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste de cartes à partir de laquelle on cherche une Paire.

        Renvois
        -------
        Paire
            Instance représentant la Paire détectée, avec ses kickers.
        """
        cls.verifier_min_cartes(cartes)
        valeurs = [c.valeur for c in cartes]
        compteur = Counter(valeurs)
        paires = [v for v, count in compteur.items() if count >= 2]
        if not paires:
            raise ValueError("Aucune Paire présente")
        meilleure_paire = max(paires, key=lambda v: Carte.VALEURS().index(v))

        cartes_restantes = [v for v in valeurs if v != meilleure_paire]
        kickers = sorted(cartes_restantes, key=lambda v: Carte.VALEURS().index(v), reverse=True)

        return cls(hauteur=meilleure_paire, kicker=kickers)

    def __str__(self) -> str:
        """
        Renvoie une représentation textuelle lisible de la Paire.

        Renvois
        -------
        str
            Exemple : "Paire As et Roi" si kicker, sinon "Paire As".
        """
        if self.hauteur == "As":
            return "Paire d'As"
        else:
            return f"Paire {self.hauteur}"

    def __repr__(self) -> str:
        """
        Renvoie une représentation technique de la Paire

        Renvois
        -------

        """
        return f"Paire(hauteur={self.hauteur}, kicker={self.kicker})"
