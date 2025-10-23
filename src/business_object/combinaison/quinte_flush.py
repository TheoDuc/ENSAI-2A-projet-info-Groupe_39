from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class QuinteFlush(AbstractCombinaison):
    """Classe représentant une Quinte Flush (suite de 5 cartes de même couleur)."""

    def __init__(self, hauteur: str):
        """
        Initialise une combinaison Quinte Flush.

        Paramètres
        ----------
        hauteur : str
            Valeur de la carte la plus haute de la Quinte Flush.

        """
        super().__init__(hauteur, kicker=None)

    @classmethod
    def FORCE(cls) -> int:
        """Renvoie la force hiérarchique de la combinaison Quinte Flush (8)."""
        return 8

    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        """
        Vérifie si une Quinte Flush est présente dans une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste d’objets Carte à analyser.

        Renvois
        -------
        bool
            True si une Quinte Flush est détectée, False sinon.
        """
        if len(cartes) < 5:
            return False

        couleurs = [c.couleur for c in cartes]
        for couleur in set(couleurs):
            cartes_couleur = [c for c in cartes if c.couleur == couleur]
            indices = sorted([Carte.VALEURS().index(c.valeur) for c in cartes_couleur])
            for i in range(len(indices) - 4):
                if indices[i + 4] - indices[i] == 4:
                    return True
        return False

    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "QuinteFlush":
        """
        Construit une instance de Quinte Flush à partir d’une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste de cartes à partir de laquelle on cherche une Quinte Flush.

        Renvois
        -------
        QuinteFlush
            Instance représentant la Quinte Flush détectée.

        Exceptions
        ----------
        ValueError
            Si aucune Quinte Flush n’est trouvée dans les cartes.
        """
        couleurs = [c.couleur for c in cartes]
        for couleur in set(couleurs):
            cartes_couleur = [c for c in cartes if c.couleur == couleur]
            indices = sorted(
                [Carte.VALEURS().index(c.valeur) for c in cartes_couleur], reverse=True
            )
            for i in range(len(indices) - 4):
                if indices[i] - indices[i + 4] == 4:
                    hauteur = Carte.VALEURS()[indices[i]]
                    return cls(hauteur)
        raise ValueError("Pas de quinte flush dans ces cartes")

    def __str__(self) -> str:
        """
        Renvoie une représentation textuelle lisible de la Quinte Flush.

        Renvois
        -------
        str
            Exemple : "Quinte Flush As".
        """
        return f"Quinte Flush {self.hauteur}"

    def __repr__(self) -> str:
        """
        Renvoie une représentation technique de la Quinte Flush

        Renvois
        -------

        """
        return str(self)
