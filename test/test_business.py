import os

import pytest


def test_calculate(get_PrepareSalary):
    p = get_PrepareSalary
    assert p.gross == 3000
    assert p.net == 3000
    assert p.invest == 3
    assert p.big_save == 150
