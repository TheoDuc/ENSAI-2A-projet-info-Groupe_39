from collections import Counter
from typing import List, Tuple

from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Full(AbstractCombinaison):
    """Classe représentant un Full (Brelan + Paire) au poker.

    Un Full est composé d’un Brelan (trois cartes de même valeur) et
    d’une Paire (deux cartes de même valeur différente du Brelan).
    La comparaison se fait d’abord sur le Brelan, puis sur la Paire.
    """

    def __init__(self, hauteur: str, cartes: List[Carte] = None, kicker: Tuple[str, ...] = None):
        """
        Initialise une combinaison Full.

        Paramètres
        ----------
        hauteur : str
            Valeur du Brelan.
        cartes : list[Carte], optionnel
            Liste des cartes formant le Full (doit contenir 5 cartes si fournie).
        kicker : tuple[str, ...], optionnel
            Non utilisé, inclus pour compatibilité avec AbstractCombinaison.
        """
        if cartes is not None and len(cartes) not in (0, 5):
            raise ValueError(f"Un Full doit contenir 5 cartes, reçu {len(cartes)}")

        kicker = None
        super().__init__(hauteur, kicker)
        self.cartes = cartes or []
        self._brelan = None
        self._paire = None

        # Détection automatique si cartes fournies
        if self.cartes:
            valeurs = [c.valeur for c in self.cartes]
            compteur = Counter(valeurs)
            brelans = [v for v in compteur if compteur[v] >= 3]
            if brelans:
                self._brelan = max(brelans, key=lambda x: Carte.VALEURS().index(x))
            valeurs_paires = [v for v in compteur if compteur[v] >= 2 and v != self._brelan]
            if valeurs_paires:
                self._paire = max(valeurs_paires, key=lambda x: Carte.VALEURS().index(x))

    @property
    def paire(self):
        """Renvoie la valeur de la Paire du Full."""
        return self._paire

    @paire.setter
    def paire(self, valeur):
        """Définit la valeur de la Paire du Full."""
        self._paire = valeur

    @property
    def brelan(self):
        """Renvoie la valeur du Brelan du Full."""
        return self._brelan

    @brelan.setter
    def brelan(self, valeur):
        """Définit la valeur du Brelan du Full."""
        self._brelan = valeur

    @classmethod
    def FORCE(cls) -> int:
        """Renvoie la force hiérarchique de la combinaison Full (6)."""
        return 6

    @classmethod
    def est_present(cls, cartes: List[Carte]) -> bool:
        """
        Vérifie si un Full est présent dans une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste d’objets Carte à analyser.

        Renvois
        -------
        bool
            True si un Brelan et une Paire distincte sont présents, False sinon.
        """
        valeurs = [c.valeur for c in cartes]
        brelans = [v for v in set(valeurs) if valeurs.count(v) >= 3]
        paires = [v for v in set(valeurs) if valeurs.count(v) >= 2 and v not in brelans]
        return bool(brelans and paires)

    @classmethod
    def from_cartes(cls, cartes: List[Carte]) -> "Full":
        """
        Construit une instance de Full à partir d’une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste de cartes à partir de laquelle on cherche un Full.

        Renvois
        -------
        Full
            Instance représentant le Full détecté.

        Exceptions
        ----------
        ValueError
            Si aucun Brelan ou Paire n’est trouvé pour constituer le Full.
        """
        valeurs = [c.valeur for c in cartes]
        compteur = Counter(valeurs)
        brelans = [v for v in compteur if compteur[v] >= 3]
        if not brelans:
            raise ValueError(f"Aucun Brelan pour Full. Occurrences : {dict(compteur)}")
        brelan = max(brelans, key=lambda x: Carte.VALEURS().index(x))
        paires = [v for v in compteur if compteur[v] >= 2 and v != brelan]
        if not paires:
            raise ValueError(f"Aucune Paire pour Full. Occurrences : {dict(compteur)}")
        full = cls(brelan, cartes)
        full._paire = max(paires, key=lambda x: Carte.VALEURS().index(x))
        return full

    def __gt__(self, other):
        """
        Compare ce Full à un autre Full.

        Paramètres
        ----------
        other : Full
            L’autre combinaison Full à comparer.

        Renvois
        -------
        bool
            True si ce Full est plus fort que `other`, False sinon.
        """
        if not isinstance(other, Full):
            return NotImplemented
        valeurs = Carte.VALEURS()
        if valeurs.index(self.hauteur) != valeurs.index(other.hauteur):
            return valeurs.index(self.hauteur) > valeurs.index(other.hauteur)
        return valeurs.index(self._paire or "") > valeurs.index(other._paire or "")

    def __eq__(self, other):
        """
        Vérifie l’égalité avec un autre Full.


        Paramètres
        ----------
        other : Full
            L’autre Full à comparer.

        Renvois
        -------
        Full | bool
            Si égalité : un objet Full identique, sinon False.
        """
        if not isinstance(other, Full):
            return False
        if self.hauteur == other.hauteur and self._paire == other._paire:
            return Full(self.hauteur, None)
        return False

    def __str__(self):
        """
        Renvoie une représentation textuelle lisible du Full.

        Renvois
        -------
        str
            Exemple : "Full As et Roi".
        """
        return f"Full {self.hauteur} et {self._paire}"

    def __repr__(self):
        """
        Renvoie une représentation technique du Full

        Renvois
        -------

        """
        return str(self)
