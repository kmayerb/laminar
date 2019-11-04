import os
import pytest

from context import laminar
from context import laminar_examples

@pytest.fixture(scope="module")
def my_lam():
  my_lam = laminar.Laminar(2)
  return my_lam
