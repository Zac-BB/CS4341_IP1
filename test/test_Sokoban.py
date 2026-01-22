import pytest
from sokoban import Sokoban

class TestSokoban:
    
    @pytest.fixture
    def setup_teardown(self):
        model = Sokoban()
    def test_initial_value(self):
        calc = Calculator(10)
        assert calc.value == 10
    
    def test_add(self):
        calc = Calculator()
        result = calc.add(5)
        assert result == 5
        assert calc.value == 5
    
    def test_subtract(self):
        calc = Calculator(10)
        result = calc.subtract(3)
        assert result == 7