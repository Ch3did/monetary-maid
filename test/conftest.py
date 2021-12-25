import pytest
import os 
from bussines.machine.prepair_salary import PrepareSalary

import sys
sys.path.insert(0, os.path.abspath("code/pessoal/saved-future/"))


@pytest.fixture
def get_PrepareSalary():
    return PrepareSalary(3000)

