"""Implémentation des tests pour la classe Admin"""

import pytest

from business_object.admin import Admin
from business_object.joueur import Joueur


class TestAdmin:
    @pytest.fixture
    def joueur(self):
        """Fixture pour un joueur initialisé."""
        return Joueur(1, "Crocorible", 200, "France")

    def test_admin_init_succes(self):
        # GIVEN
        id_admin = 1

        # WHEN
        admin = Admin(id_admin)

        # THEN
        assert admin.id_admin == 1

    def test_admin_init_echec_TypeError(self):
        # GIVEN
        id_admin = "1"
        message_attendu = f"L'identifiant administrateur doit être un int : {type(id_admin)}"

        # WHEN / THEN
        with pytest.raises(TypeError, match=message_attendu):
            Admin(id_admin)

    def test_admin_init_ValueError(self):
        # GIVEN
        id_admin = -1
        message_attendu = (
            f"L'identifiant du joueur doit être un entier strictement positif : {id_admin}"
        )

        # WHEN / THEN
        with pytest.raises(ValueError, match=message_attendu):
            Admin(id_admin)

    def test_admin_crediter(self, joueur):
        # GIVEN
        admin = Admin(1)
        credits = 50

        # WHEN
        admin.crediter(joueur, credits)

        # THEN
        assert joueur.credit == 250

    def test_admin_debiter(self, joueur):
        # GIVEN
        admin = Admin(1)
        credits = 50

        # WHEN
        admin.debiter(joueur, credits)

        # THEN
        assert joueur.credit == 150

    def test_admin_set_credits(self, joueur):
        # GIVEN
        admin = Admin(1)
        credits = 50

        # WHEN
        admin.set_credits(joueur, credits)

        # THEN
        assert joueur.credit == 50
