from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Quinte(AbstractCombinaison):
    """Classe représentant une Quinte (suite de 5 cartes de valeurs consécutives)."""

    def __init__(self, hauteur: list[str], kicker=None):
        """
        Initialise une combinaison Quinte.

        Paramètres
        ----------
        hauteur : str
            Valeur de la carte la plus haute de la Quinte.
        """
        hauteur = sorted(hauteur, key=lambda x: Carte.VALEURS().index(x), reverse=True)
        super().__init__(hauteur, kicker)

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
        valeurs = sorted({Carte.VALEURS().index(c.valeur) for c in cartes})
        for i in range(len(valeurs) - 4):
            if valeurs[i : i + 5] == list(range(valeurs[i], valeurs[i] + 5)):
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
        cls.verifier_min_cartes(cartes)
        valeurs = sorted({Carte.VALEURS().index(c.valeur) for c in cartes})
        suites = []
        for i in range(len(valeurs) - 4):
            suite = valeurs[i : i + 5]
            if suite == list(range(suite[0], suite[0] + 5)):
                suites.append([Carte.VALEURS()[v] for v in reversed(suite)])
        if not suites:
            raise ValueError("Aucune Quinte présente.")
        meilleure_suite = max(suites, key=lambda s: Carte.VALEURS().index(s[0]))
        return cls(hauteur=meilleure_suite)

    def __str__(self) -> str:
        """
        Renvoie une représentation textuelle lisible de la Quinte.

        Renvois
        -------
        str
            Exemple : "Quinte As".
        """
        return "Quinte"

    def __repr__(self) -> str:
        """
        Renvoie une représentation technique de la Quinte

        Renvois
        -------

        """
        return f"Quinte(hauteur='{self.hauteur}')"
