import pytest
from src.model.card import Card, CardType

def test_card_is_locked():
    with pytest.raises(RuntimeError):
        Card(CardType.BLUE, 1)