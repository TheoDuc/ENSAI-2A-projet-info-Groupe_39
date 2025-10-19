from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Quinte(AbstractCombinaison):
    """Classe représentant une Quinte (suite de 5 cartes de valeurs consécutives)."""

    def __init__(self, hauteur: str, kicker=None):
        # Hauteur = carte la plus forte de la quinte
        super().__init__(hauteur, kicker)

    @classmethod
    def FORCE(cls) -> int:
        # Force relative d'une quinte dans le classement poker
        return 4

    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        """
        Vérifie si une quinte est présente.
        Étapes :
        1. Transforme les valeurs des cartes en indices numériques selon l'ordre poker.
        2. Trie les indices.
        3. Vérifie toutes les suites de 5 cartes consécutives.
        """
        valeurs_indices = sorted({Carte.VALEURS().index(c.valeur) for c in cartes})
        for i in range(len(valeurs_indices) - 4):
            if valeurs_indices[i + 4] - valeurs_indices[i] == 4:
                return True
        return False

    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "Quinte":
        """
        Construit une Quinte à partir d'une liste de cartes.
        - Cherche la suite de 5 cartes consécutives la plus forte.
        - Hauteur = carte la plus haute de la suite.
        - Lève une ValueError si aucune quinte n'est trouvée.
        """
        valeurs_indices = sorted({Carte.VALEURS().index(c.valeur) for c in cartes}, reverse=True)
        for i in range(len(valeurs_indices) - 4):
            if valeurs_indices[i] - valeurs_indices[i + 4] == 4:
                hauteur = Carte.VALEURS()[valeurs_indices[i]]
                return cls(hauteur)
        raise ValueError("Pas de quinte dans ces cartes")

    def __str__(self) -> str:
        # Représentation lisible pour le joueur, exemple : "Quinte As"
        return f"Quinte {self.hauteur}"

    def __repr__(self) -> str:
        # Représentation pour debug / tests, identique à __str__
        return str(self)
