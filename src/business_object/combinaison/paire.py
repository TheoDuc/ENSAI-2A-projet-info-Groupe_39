from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Paire(AbstractCombinaison):
    """Classe représentant une Paire (deux cartes de même valeur) au poker."""

    def __init__(self, hauteur: str, kicker: tuple[str, ...]):
        """
        Initialise une combinaison Paire.

        Paramètres
        ----------
        hauteur : str
            Valeur de la Paire.
        kicker : tuple[str, ...]
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
        return any(valeurs.count(v) == 2 for v in set(valeurs))

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
        valeurs = [c.valeur for c in cartes]

        paire = max(
            [v for v in set(valeurs) if valeurs.count(v) == 2],
            key=lambda x: Carte.VALEURS().index(x),
        )

        kicker = tuple(
            sorted(
                [v for v in valeurs if v != paire],
                key=lambda x: Carte.VALEURS().index(x),
                reverse=True,
            )
        )

        return cls(paire, kicker)

    def __str__(self):
        """
        Renvoie une représentation textuelle lisible de la Paire.

        Renvois
        -------
        str
            Exemple : "Paire As et Roi" si kicker, sinon "Paire As".
        """
        return (
            f"Paire {self.hauteur} et {self.kicker[0]}" if self.kicker else f"Paire {self.hauteur}"
        )

    def __repr__(self):
        """
        Renvoie une représentation technique de la Paire

        Renvois
        -------

        """
        return f"Paire(hauteur={self.hauteur}, kicker={self.kicker})"
