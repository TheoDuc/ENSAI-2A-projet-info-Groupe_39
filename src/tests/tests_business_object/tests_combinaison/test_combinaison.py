"""Implémentation des tests pour la classe AbstractCombinaison"""

from abc import ABC

import pytest

from business_object.combinaison import AbstractCombinaison

class AbstractCombinaisonTest(ABC):
    @pytest.fixture
    def cls(self):
        return NotImplementedError

    