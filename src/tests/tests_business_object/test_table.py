"""Implémentation des tests pour la classe Table"""

import pytest

from business_object.table import Table
from business_object.joueur import Joueur


class Test:
    def test_table_len_succes(self):
        # GIVEN
        table = Table(10,10,1,[])
        taille_attendu = 0
        
        # WHEN
        taille = len(table)

        # THEN
        assert taille == taille_attendu

    def test_table_ajoute_joueur_succes(self):
        # GIVEN
        table = Table(10,10,1,[])
        joueur = Joueur(1, "alice", 1000, True, "France", 20)
        table_attendu = Table(10,10,1,[joueur])

        # WHEN
        table.ajouter_joueur(joueur)

        # THEN
        assert len(table) == len(table_attendu)
        assert table.joueurs == table_attendu.joueurs

    def test_table_ajouter_joueur_valeur_incorrecte(self):
        # GIVEN
        joueur = Joueur(1, "alice", 1000, True, "France", 20)
        table = Table(1,10,1,[joueur])
        message_attendu = "Nombre maximum de joueurs atteint"

        # WHEN / THEN
        with pytest.raises(ValueError, match=message_attendu):
            table.ajouter_joueur(joueur)

    def test_table_retirer_joueur_succes(self):
        # GIVEN
        table_attendu = Table(10,10,1,[])
        joueur = Joueur(1, "alice", 1000, True, "France", 20)
        table = Table(10,10,1,[joueur])
        indice = 0

        # WHEN
        table.retirer_joueur(indice)

        # THEN
        assert len(table) == len(table_attendu)
        assert table.joueurs == table_attendu.joueurs

    def test_table_retirer_joueur_valeur_incorrecte(self):
        # GIVEN
        table = Table(1,10,1,[])
        message_attendu = "Indice de joueur incorrect"
        indice = -6

        # WHEN / THEN
        with pytest.raises(IndexError, match=message_attendu):
            table.retirer_joueur(indice)

    def test_table_retirer_joueur_valeur_incorrecte2(self):
        # GIVEN
        table = Table(1,10,1,[])
        message_attendu = "Indice de joueur incorrect"
        indice = 2

        # WHEN / THEN
        with pytest.raises(IndexError, match=message_attendu):
            table.retirer_joueur(indice)

    def test_table_mettre_grosse_blind_succes(self):
        # GIVEN
        
        # WHEN

        # THEN
        assert True == True

    def test_table_rotation_dealer_succes(self):
        # GIVEN
        
        # WHEN

        # THEN
        assert True == True

    def test_table_lancer_manche_succes(self):
        # GIVEN
        
        # WHEN

        # THEN
        assert True == True
