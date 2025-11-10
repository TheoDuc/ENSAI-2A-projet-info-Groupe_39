from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Union

from business_object.carte import Carte


class AbstractCombinaison(ABC):
    """
    Classe abstraite représentant une combinaison de cartes au poker.

    Paramètres
    ----------
    hauteur : str | tuple[str, ...] | list[str]
        Représente la ou les cartes principales de la combinaison.

    kicker : str | tuple[str, ...] | list[str] | None, optionnel
        Cartes d’appoint utilisées pour départager deux mains identiques.
        Si non fourni, le kicker est vide.

    Attributs
    ----------
    _hauteur : str | list[str]
        Hauteur principale de la combinaison (str si une seule valeur, liste sinon).
    _kicker : tuple[str, ...]
        Ensemble immuable représentant les cartes de départage.
    """

    def __init__(
        self,
        hauteur: Union[str, Tuple[str, ...], list[str]],
        kicker: Optional[Union[str, Tuple[str, ...], list[str]]] = None,
    ) -> None:
        if isinstance(hauteur, (list, tuple)):
            if len(hauteur) == 1:
                hauteur = hauteur[0]
            else:
                hauteur = list(hauteur)
        elif not isinstance(hauteur, str):
            raise TypeError("La hauteur doit être un str, une liste ou un tuple.")

        if kicker is None:
            self._kicker = ()
        elif isinstance(kicker, str):
            self._kicker = (kicker,)
        elif isinstance(kicker, (list, tuple)):
            self._kicker = tuple(kicker)  # toujours en tuples
        else:
            raise TypeError("Le kicker doit être un str, une liste, un tuple ou None.")

        self._hauteur = hauteur

    def verifier_min_cartes(cartes: list, n: int = 5) -> None:
        """
        Vérifie que la liste de cartes contient au moins `n` cartes.

        Paramètres
        ----------
        cartes : list
            Liste de cartes à vérifier.
        n : int
            Nombre minimal de cartes requis (par défaut 5).

        Raises
        ------
        ValueError
            Si le nombre de cartes est inférieur à `n`.
        """
        if len(cartes) < n:
            raise ValueError(f"Il faut au moins {n} cartes pour évaluer cette combinaison.")

    @property
    def hauteur(self) -> Union[str, List[str]]:
        if isinstance(self._hauteur, (list, tuple)):
            if len(self._hauteur) == 1:
                return self._hauteur[0]
            return list(self._hauteur)
        return self._hauteur

    @property
    def kicker(self) -> Optional[Union[str, Tuple[str, ...]]]:
        if not self._kicker:
            return None
        # si c'est un tuple d'une seule valeur, retourne la valeur simple
        if isinstance(self._kicker, tuple) and len(self._kicker) == 1:
            return self._kicker[0]
        return self._kicker

    # --- Méthodes abstraites ---
    @classmethod
    @abstractmethod
    def FORCE(cls) -> int:
        pass

    @classmethod
    @abstractmethod
    def est_present(cls, cartes: List[Carte]) -> bool:
        pass

    @classmethod
    @abstractmethod
    def from_cartes(cls, cartes: List[Carte]) -> "AbstractCombinaison":
        pass

    def _valeur_comparaison(self) -> Tuple[int, Tuple[int, ...], Tuple[int, ...]]:
        """Renvoie la valeur numérique de comparaison de la combinaison."""

        # Hauteur → normalisation en tuple d'indices
        if isinstance(self._hauteur, (list, tuple)):
            hauteur_vals = tuple(Carte.VALEURS().index(h) for h in self._hauteur)
        else:
            hauteur_vals = (Carte.VALEURS().index(self._hauteur),)

        # Kicker → peut être vide
        if not self._kicker:
            kicker_vals = ()
        elif isinstance(self._kicker, (list, tuple)):
            kicker_vals = tuple(Carte.VALEURS().index(k) for k in self._kicker)
        else:
            kicker_vals = (Carte.VALEURS().index(self._kicker),)
        return (self.FORCE(), hauteur_vals, kicker_vals)

    def __eq__(self, other) -> bool:
        if not isinstance(other, AbstractCombinaison):
            return NotImplemented
        return self._valeur_comparaison() == other._valeur_comparaison()

    def __lt__(self, other) -> bool:
        if not isinstance(other, AbstractCombinaison):
            return NotImplemented
        return self._valeur_comparaison() < other._valeur_comparaison()

    # --- Représentations ---

    def _fmt_valeurs(self, val) -> Optional[str]:
        """Convertit tuple/liste -> string propre pour l'affichage."""
        if val is None:
            return None
        if isinstance(val, (tuple, list)):
            if len(val) == 1:
                return val[0]
            return " et ".join(val)
        return val

    def __str__(self) -> str:
        nom = self.__class__.__name__
        h = self._fmt_valeurs(self.hauteur)
        if h == "As":
            return f"{nom} d'{h}"
        return f"{nom} de {h}"

    def __repr__(self) -> str:
        h = self._fmt_valeurs(self.hauteur)
        k = self._fmt_valeurs(self.kicker)
        if not self._kicker:
            return f"{self.__class__.__name__}(hauteur={h})"
        return f"{self.__class__.__name__}(hauteur={h}, kicker={k})"
