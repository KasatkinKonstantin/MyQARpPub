import pytest
from app.calculator import Calculator

class TestCalc:
    def setup(self):
        self.calc = Calculator

    def test_multiply_passed(self):
        assert self.calc.multiply(self, 2, 2) == 4

    def test_division_passed(self):
        assert self.calc.division(self, 10, 5) == 2

    def test_subtraction_passed(self):
        assert self.calc.subtraction(self, 12, 10) == 2

    def test_adding_passed(self):
        assert self.calc.adding(self, 3, 4) == 7



