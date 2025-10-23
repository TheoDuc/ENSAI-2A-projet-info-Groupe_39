from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Quinte(AbstractCombinaison):
    """Classe représentant une Quinte (suite de 5 cartes de valeurs consécutives)."""

    def __init__(self, hauteur: str):
        """
        Initialise une combinaison Quinte.

        Paramètres
        ----------
        hauteur : str
            Valeur de la carte la plus haute de la Quinte.
        """
        super().__init__(hauteur, kicker=None)

    @classmethod
    def FORCE(cls) -> int:
        """Renvoie la force hiérarchique de la combinaison Quinte (4)."""
        return 4

    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        """
        Vérifie si une Quinte est présente dans une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste d’objets Carte à analyser.

        Renvois
        -------
        bool
            True si une suite de 5 cartes consécutives est détectée, False sinon.
        """
        valeurs_indices = sorted({Carte.VALEURS().index(c.valeur) for c in cartes})
        for i in range(len(valeurs_indices) - 4):
            if valeurs_indices[i + 4] - valeurs_indices[i] == 4:
                return True
        return False

    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "Quinte":
        """
        Construit une instance de Quinte à partir d’une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste de cartes à partir de laquelle on cherche une Quinte.

        Renvois
        -------
        Quinte
            Instance représentant la Quinte détectée.

        Exceptions
        ----------
        ValueError
            Si aucune Quinte n’est trouvée dans les cartes.
        """
        valeurs_indices = sorted({Carte.VALEURS().index(c.valeur) for c in cartes}, reverse=True)
        for i in range(len(valeurs_indices) - 4):
            if valeurs_indices[i] - valeurs_indices[i + 4] == 4:
                hauteur = Carte.VALEURS()[valeurs_indices[i]]
                return cls(hauteur)
        raise ValueError("Pas de quinte dans ces cartes")

    def __str__(self) -> str:
        """
        Renvoie une représentation textuelle lisible de la Quinte.

        Renvois
        -------
        str
            Exemple : "Quinte As".
        """
        return f"Quinte {self.hauteur}"

    def __repr__(self) -> str:
        """
        Renvoie une représentation technique de la Quinte

        Renvois
        -------

        """
        return str(self)
