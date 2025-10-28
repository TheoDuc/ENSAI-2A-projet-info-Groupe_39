from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class QuinteFlush(AbstractCombinaison):
    """Classe représentant une Quinte Flush (suite de 5 cartes de même couleur)."""

    def __init__(self, hauteur: list[str], kicker=None):
        """
        Initialise une combinaison Quinte Flush.

        Paramètres
        ----------
        hauteur : list[str]
            Liste des valeurs des cartes formant la Quinte Flush, de la plus haute à la plus basse.


        """
        hauteur = sorted(hauteur, key=lambda x: Carte.VALEURS().index(x), reverse=True)
        super().__init__(hauteur, kicker)

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

        meilleures_suites = []
        for i in range(len(valeurs) - 4):
            suite = valeurs[i : i + 5]
            if suite == list(range(suite[0], suite[0] + 5)):
                meilleures_suites.append([Carte.VALEURS()[v] for v in reversed(suite)])
        if not meilleures_suites:
            raise ValueError("Aucune Quinte Flush présente.")
        meilleure_suite = max(meilleures_suites, key=lambda s: Carte.VALEURS().index(s[0]))

        return cls(hauteur=meilleure_suite)

    def __str__(self) -> str:
        """
        Renvoie une représentation textuelle lisible de la Quinte Flush.

        Renvois
        -------
        str
            Exemple : "Quinte Flush As".
        """
        if self.hauteur[0] == "As":
            return "QuinteFlush Royale"
        return "Quinte Flush"

    def __repr__(self) -> str:
        """
        Renvoie une représentation technique de la Quinte Flush

        Renvois
        -------

        """
        return f"QuinteFlush(hauteur={self.hauteur})"
