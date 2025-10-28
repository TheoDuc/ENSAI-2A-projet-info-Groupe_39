from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class QuinteFlush(AbstractCombinaison):
    """Classe représentant une Quinte Flush (suite de 5 cartes de même couleur)."""

    def __init__(self, hauteur: str, kicker):
        """
        Initialise une combinaison Quinte Flush.

        Paramètres
        ----------
        hauteur : list[str]
            Liste des valeurs des cartes formant la Quinte Flush, de la plus haute à la plus basse.


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
        couleurs = [c.couleur for c in cartes]
        couleur_max = next((c for c in set(couleurs) if couleurs.count(c) >= 5), None)
        if not couleur_max:
            return False

        cartes_couleur = [c for c in cartes if c.couleur == couleur_max]
        valeurs = sorted([Carte.VALEURS().index(c.valeur) for c in cartes_couleur])
        for i in range(len(valeurs) - 4):
            if valeurs[i : i + 5] == list(range(valeurs[i], valeurs[i] + 5)):
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
        cls.verifier_min_cartes(cartes)
        couleurs = [c.couleur for c in cartes]
        couleur_max = next((c for c in set(couleurs) if couleurs.count(c) >= 5), None)
        if not couleur_max:
            raise ValueError("Aucune couleur avec les 5 cartes.")

        cartes_couleur = [c for c in cartes if c.couleur == couleur_max]
        valeurs = sorted([Carte.VALEURS().index(c.valeur) for c in cartes_couleur])

        cls.verifier_min_cartes(cartes)
        valeurs = sorted({Carte.VALEURS().index(c.valeur) for c in cartes})
        suites = []
        for i in range(len(valeurs) - 4):
            suite = valeurs[i : i + 5]
            if suite == list(range(suite[0], suite[0] + 5)):
                suites.append(suite)
        if not suites:
            raise ValueError("Aucune Quinte Flush présente.")
        # On prend la carte la plus haute de la meilleure suite
        max_suite = max(suites, key=lambda s: s[-1])
        hauteur = Carte.VALEURS()[max_suite[-1]]
        return cls(hauteur=hauteur)

    def __str__(self) -> str:
        """
        Renvoie une représentation textuelle lisible de la Quinte Flush.

        Renvois
        -------
        str
            Exemple : "Quinte Flush As".
        """
        if self.hauteur[0] == "As":
            return "Quinte Flush Royale"
        return "Quinte Flush"

    def __repr__(self) -> str:
        """
        Renvoie une représentation technique de la Quinte Flush

        Renvois
        -------

        """
        return f"Quinte Flush(hauteur={self.hauteur})"
