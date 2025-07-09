from astropy import units as u
from numpy.testing import assert_allclose

from boinor.core.earth_atmosphere.util import (
    _check_altitude,
    gravity,
    h_to_z,
    z_to_h,
)


def test_earth_athmosphere_util():
    g0 = 9.81 * u.m / (u.s * u.s)
    r0 = 6000 * u.km
    z = 100
    alt = 100
    expected_h = 98.360656
    expected_g = 9.490997

    h = z_to_h(z, r0)
    assert_allclose(expected_h, h)

    z_new = h_to_z(h, r0)
    assert_allclose(z_new, z)

    g = gravity(z, g0, r0)
    assert_allclose(expected_g, g)

    vn_z, vn_h = _check_altitude(alt, r0, True)
    assert_allclose(alt, vn_z)
    assert_allclose(z_to_h(alt, r0), vn_h)

    vn2_z, vn2_h = _check_altitude(alt, r0, False)
    assert_allclose(h_to_z(alt, r0), vn2_z)
    assert_allclose(alt, vn2_h)
