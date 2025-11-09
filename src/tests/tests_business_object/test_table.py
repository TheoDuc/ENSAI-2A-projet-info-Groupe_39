"""Implémentation des tests pour la classe Table"""

import pytest

from business_object.joueur import Joueur
from business_object.table import Table


class TestTable:
    @pytest.fixture
    def alice(self):
        return Joueur(1, "alice", 1000, "France")

    @pytest.fixture
    def bernard(self):
        return Joueur(2, "bernard", 500, "France")

    def test_table_len_succes(self):
        # GIVEN
        table = Table(8, 40)
        taille_attendu = 0

        # WHEN
        taille = len(table)

        # THEN
        assert taille == taille_attendu

    def test_table_ajoute_joueur_succes(self, alice):
        # GIVEN
        table = Table(10, 10)
        joueur = alice
        liste_joueurs = [alice]

        # WHEN
        table.ajouter_joueur(joueur)

        # THEN
        assert len(table) == 1
        assert table.joueurs == liste_joueurs

    def test_table_ajouter_joueur_type_incorrecte(self):
        # GIVEN
        joueur = (1, "alice", 1000, True, "France", 20)
        table = Table(1, 10, 1, [])
        message_attendu = "Le joueur n'est pas une instance de joueur"

        # WHEN / THEN
        with pytest.raises(TypeError, match=message_attendu):
            table.ajouter_joueur(joueur)

    def test_table_ajouter_joueur_valeur_incorrecte(self, alice):
        # GIVEN
        joueur = alice
        table = Table(2, 10, joueurs=[alice, alice])
        message_attendu = "Nombre maximum de joueurs atteint"

        # WHEN / THEN
        with pytest.raises(ValueError, match=message_attendu):
            table.ajouter_joueur(joueur)

    def test_table_retirer_joueur_succes(self, alice):
        # GIVEN
        joueur = alice
        table = Table(10, 10, joueurs=[alice])
        table_attendu = Table(10, 10, 1, [])
        indice = 0

        # WHEN
        joueur_supprime = table.retirer_joueur(indice)

        # THEN
        assert len(table) == len(table_attendu)
        assert table.joueurs == table_attendu.joueurs
        assert joueur_supprime == joueur

    def test_table_retirer_joueur_valeur_incorrecte(self):
        # GIVEN
        table = Table(1, 10, 1, [])
        message_attendu = "Indice négatif impossible"
        indice = -6

        # WHEN / THEN
        with pytest.raises(IndexError, match=message_attendu):
            table.retirer_joueur(indice)

    def test_table_retirer_joueur_valeur_incorrecte2(self):
        # GIVEN
        table = Table(1, 10, 1, [])
        message_attendu = f"Indice plus grand que le nombre de joueurs : {len(table.joueurs)}"
        indice = 2

        # WHEN / THEN
        with pytest.raises(IndexError, match=message_attendu):
            table.retirer_joueur(indice)

    def test_table_retirer_joueur_valeur_incorrecte3(self):
        # GIVEN
        table = Table(1, 10, 1, [])
        message_attendu = "L'indice doit être un entier"
        indice = "a"

        # WHEN / THEN
        with pytest.raises(TypeError, match=message_attendu):
            table.retirer_joueur(indice)

    def test_table_mettre_grosse_blind_succes(self, alice):
        # GIVEN
        joueur1 = alice
        table = Table(10, 10, 1, [joueur1])
        credit = 50

        # WHEN
        table.mettre_grosse_blind(credit)

        # THEN
        assert table.grosse_blind == credit

    def test_table_mettre_grosse_blind_valeur_incorrecte3(self):
        # GIVEN
        table = Table(1, 10, 1, [])
        message_attendu = "Le crédit doit être un entier"
        credit = "a"

        # WHEN / THEN
        with pytest.raises(TypeError, match=message_attendu):
            table.mettre_grosse_blind(credit)

    def test_table_rotation_dealer_succes(self, alice, bernard):
        # GIVEN
        joueur1 = alice
        joueur2 = bernard
        table = Table(10, 10, joueurs=[joueur1, joueur2])
        table_attendue = Table(10, 10, joueurs=[joueur2, joueur1])

        # WHEN
        table.rotation_dealer()

        # THEN
        assert table.joueurs == table_attendue.joueurs

    def test_table_lancer_manche_succes(self):
        # GIVEN

        # WHEN

        # THEN
        assert True
