from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class DoublePaire(AbstractCombinaison):
    """
    Classe représentant une combinaison *Double Paire* (deux paires de cartes de même valeur).

    La combinaison est caractérisée par :
    - la hauteur de la paire la plus forte,
    - la hauteur de la deuxième paire (utilisée comme kicker),
    - et éventuellement la carte restante servant de kicker supplémentaire.
    """

    def __init__(self, hauteur: str, kicker: tuple[str, ...]):
        """
        Initialise une combinaison Double Paire.

        Paramètres
        ----------
        hauteur : str
            Valeur de la paire la plus forte (ex. 'Roi').
        kicker : tuple[str, ...]
            Tuple contenant la valeur de la deuxième paire et éventuellement
            la carte restante servant de kicker.
        """
        super().__init__(hauteur, kicker)

    @classmethod
    def FORCE(cls) -> int:
        """
        Renvoie la force hiérarchique de la combinaison *Double Paire*.

        Renvois
        -------
        int
            Valeur entière représentant la force de la combinaison.

        """
        return 2

    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        """
        Vérifie si une Double Paire est présente dans une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste d’objets Carte représentant la main à analyser.

        Renvois
        -------
        bool
            True si au moins deux valeurs apparaissent au moins deux fois, False sinon.


        """
        valeurs = [c.valeur for c in cartes]
        return len([v for v in set(valeurs) if valeurs.count(v) >= 2]) >= 2

    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "DoublePaire":
        """
        Construit une instance de Double Paire à partir d’une liste de cartes.

        Recherche les deux paires les plus fortes et détermine le kicker
        éventuel (la carte la plus haute restante).

        Paramètres
        ----------
        cartes : list[Carte]
            Liste d’objets Carte pour générer la combinaison.

        Renvois
        -------
        DoublePaire
            Instance de la combinaison avec la paire la plus forte et le kicker calculé.

        Exceptions
        ----------
        ValueError
            Si moins de deux paires sont présentes dans la main.


        """

        valeurs = [c.valeur for c in cartes]

        paires = sorted(
            [v for v in set(valeurs) if valeurs.count(v) >= 2],
            key=lambda x: Carte.VALEURS().index(x),
            reverse=True,
        )

        if len(paires) < 2:
            raise ValueError("Pas assez de paires pour créer une Double Paire")

        kickers = [v for v in valeurs if v not in paires]
        kicker_supp = sorted(kickers, key=lambda x: Carte.VALEURS().index(x), reverse=True)
        kicker = (paires[1], kicker_supp[0]) if kicker_supp else (paires[1],)

        return cls(paires[0], kicker)

    def __str__(self):
        """
        Renvoie une représentation textuelle lisible de la Double Paire.

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        str
            Chaîne lisible par un joueur, par exemple :
            "Double Paire Roi et Dame".
        """
        return f"Double Paire {self.hauteur} et {self.kicker[0]}"

    def __repr__(self) -> str:
        """
        Renvoie une représentation technique de la Double Paire

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        str
            Exemple : "DoublePaire(hauteur=Roi, kicker=(Dame, 9))".
        """
        kicker_str = ", ".join(self.kicker)
        return f"DoublePaire(hauteur={self.hauteur}, kicker=({kicker_str}))"
