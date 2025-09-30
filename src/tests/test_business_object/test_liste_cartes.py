"""Implémentation des tests pour la classe AbstractListeCartes"""

from abc import ABC

import pytest

from business_object.liste_cartes import AbstractListeCartes


class AbstractListeCartesTest(ABC):
    @pytest.fixture
    def liste_cartes(self) -> AbstractListeCartes:
        """
        Fixture à implémenter dans les sous-classes.

        IMPORTANT :
        Chaque sous-classe doit fournir une liste contenant exactement deux cartes :
        - As de pique
        - 10 de coeur
        """
        raise NotImplementedError

    def test_liste_cartes_str(self, liste_cartes):
        # GIVEN
        # liste_carte en fixture

        # WHEN
        affichage = str(liste_cartes)

        # THEN
        assert affichage == "[As de pique, 10 de coeur]"

    def test_liste_cartes_len(self, liste_cartes):
        # GIVEN
        # liste_carte en fixture

        # WHEN
        longueur = len(liste_cartes)

        # THEN
        assert longueur == 2

    def test_liste_cartes_ajouter_carte_succes(self, liste_cartes):
        # GIVEN
        # liste_carte en fixture
        carte = pytest.cinq_trefle

        # WHEN
        liste_cartes.ajouter_carte(carte)

        # THEN
        assert liste_cartes.cartes[-1] == carte
        assert len(liste_cartes) == 3

    def test_liste_cartes_ajouter_carte_echec(self, liste_cartes):
        # GIVEN
        # liste_cartes en fixture
        carte = 2
        message_attendu = f"l'objet à ajouter n'est pas de type Carte : {type(carte)}"

        # WHEN / THEN
        with pytest.raises(TypeError, match=message_attendu):
            liste_cartes.ajouter_carte(carte)

    def test_liste_cartes_retirer_carte_succes(self, liste_cartes):
        # GIVEN
        # liste_cartes en fixture

        # WHEN
        carte_retiree = liste_cartes.retirer_carte()

        # THEN
        assert carte_retiree == pytest.as_pique
        assert len(liste_cartes) == 1

    def test_liste_cartes_retirer_carte_indice_non_int(self, liste_cartes):
        # GIVEN
        # liste_cartes en fixture
        indice = "1"
        message_attendu = f"L'indice renseigné n'est pas de type int : {type(indice)}"

        # WHEN / THEN
        with pytest.raises(TypeError, match=message_attendu):
            liste_cartes.retirer_carte(indice)

    def test_liste_cartes_retirer_carte_indice_trop_grand(self, liste_cartes):
        # GIVEN
        # liste_cartes en fixture
        indice = 2
        message_attendu = f"L'indice renseigné est trop grand : {indice}"

        # WHEN / THEN
        with pytest.raises(ValueError, match=message_attendu):
            liste_cartes.retirer_carte(indice)

    def test_liste_cartes_trie_valeur_croissant(self, liste_cartes):
        # GIVEN
        # liste_cartes en fixture

        # WHEN
        liste_cartes.trie_valeur()

        # THEN
        assert liste_cartes.cartes[0] == pytest.dix_coeur

    def test_liste_cartes_trie_valeur_croissante(self, liste_cartes):
        # GIVEN
        # liste_cartes en fixture
        croissant = False

        # WHEN
        liste_cartes.trie_valeur(croissant)

        # THEN
        assert liste_cartes.cartes[0] == pytest.as_pique
