from abc import ABC, abstractmethod
from functools import total_ordering
from typing import List, Optional, Tuple, Union

from business_object.carte import Carte


@total_ordering
class AbstractCombinaison(ABC):
    """
    Classe de base pour toutes les combinaisons de cartes au poker.

    Chaque combinaison est caractérisée par :
    - une ou plusieurs cartes principales ("hauteur"),
    - un ou plusieurs kickers pour départager des mains identiques.
    """

    def __init__(
        self,
        hauteur: Union[str, Tuple[str, ...], List[str]],
        kicker: Optional[Union[str, Tuple[str, ...], List[str]]] = None,
    ) -> None:
        # Normalisation de la hauteur
        if isinstance(hauteur, (list, tuple)):
            hauteur = hauteur[0] if len(hauteur) == 1 else list(hauteur)
        elif not isinstance(hauteur, str):
            raise TypeError("La hauteur doit être un str, une liste ou un tuple.")

        # Normalisation du kicker
        if kicker is None:
            self._kicker = ()
        elif isinstance(kicker, str):
            self._kicker = (kicker,)
        elif isinstance(kicker, (list, tuple)):
            self._kicker = tuple(kicker)
        else:
            raise TypeError("Le kicker doit être un str, une liste, un tuple ou None.")

        self._hauteur = hauteur

    @staticmethod
    def verifier_min_cartes(cartes: list, n: int = 5) -> None:
        """
        Vérifie que la liste de cartes contient au moins `n` cartes.

        Raises
        ------
        ValueError
            Si le nombre de cartes est inférieur à `n`.
        """
        if len(cartes) < n:
            raise ValueError(f"Au moins {n} cartes sont nécessaires pour cette combinaison.")

    @property
    def hauteur(self) -> Union[str, List[str]]:
        """Retourne la ou les cartes principales de la combinaison."""
        if isinstance(self._hauteur, (list, tuple)):
            return self._hauteur[0] if len(self._hauteur) == 1 else list(self._hauteur)
        return self._hauteur

    @property
    def kicker(self) -> Optional[Union[str, Tuple[str, ...]]]:
        """Retourne les kickers sous forme de valeur unique ou de tuple."""
        if not self._kicker:
            return None
        return self._kicker[0] if len(self._kicker) == 1 else self._kicker

    # --- Méthodes abstraites ---
    @classmethod
    @abstractmethod
    def FORCE(cls) -> int:
        """Renvoie la force de la combinaison pour comparaison."""
        pass

    @classmethod
    @abstractmethod
    def est_present(cls, cartes: List[Carte]) -> bool:
        """Indique si la combinaison est présente dans une liste de cartes."""
        pass

    @classmethod
    @abstractmethod
    def from_cartes(cls, cartes: List[Carte]) -> "AbstractCombinaison":
        """Construit une instance de la combinaison à partir d’une liste de cartes."""
        pass

    # --- Comparaison entre combinaisons ---
    def _valeur_comparaison(self) -> Tuple[int, Tuple[int, ...], Tuple[int, ...]]:
        """Renvoie les valeurs numériques pour comparer deux combinaisons."""
        # Hauteur → indices
        if isinstance(self._hauteur, (list, tuple)):
            hauteur_vals = tuple(Carte.VALEURS().index(h) for h in self._hauteur)
        else:
            hauteur_vals = (Carte.VALEURS().index(self._hauteur),)

        # Kicker → indices
        if not self._kicker:
            kicker_vals = ()
        else:
            kicker_vals = tuple(Carte.VALEURS().index(k) for k in self._kicker)

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
        """Convertit un tuple ou une liste en chaîne lisible."""
        if val is None:
            return None
        if isinstance(val, (tuple, list)):
            return val[0] if len(val) == 1 else " et ".join(val)
        return val

    def __str__(self) -> str:
        h = self._fmt_valeurs(self.hauteur)
        nom = self.__class__.__name__
        return f"{nom} d'{h}" if h == "As" else f"{nom} de {h}"

    def __repr__(self) -> str:
        h = self._fmt_valeurs(self.hauteur)
        k = self._fmt_valeurs(self.kicker)
        return (
            f"{self.__class__.__name__}(hauteur={h})"
            if not self._kicker
            else f"{self.__class__.__name__}(hauteur={h}, kicker={k})"
        )
