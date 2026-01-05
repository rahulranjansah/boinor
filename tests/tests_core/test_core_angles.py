"""test angles from core sub-package angles"""
import numpy as np
import pytest

from boinor.core.angles import M_to_E_vector

# lots of functions are already checked somewhere else


def test_vector_func():
    M = np.array([1, 2, 3, 4])
    ecc = np.array([5, 6, 7, 8])
    ecc_short = np.array([5, 6, 7])

    # vectores have the same length, no error should occur
    _ = M_to_E_vector(M, ecc)

    # different vector lengths are not good
    with pytest.raises(ValueError, match=""):
        _ = M_to_E_vector(M, ecc_short)
