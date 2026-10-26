import pytest

from acam.propagation import air_absorption, level_at


@pytest.mark.parametrize("freq, db_per_km", [(1000, 5.0), (2000, 9.0), (4000, 22.9), (8000, 76.6)])
def test_air_absorption_matches_the_iso_table_at_20c_70_percent(freq, db_per_km):
    # ISO 9613-2 Table 2, 20 deg C, 70 % relative humidity.
    assert air_absorption(freq) * 1000 == pytest.approx(db_per_km, rel=0.05)


def test_dry_air_eats_more_high_notes():
    assert air_absorption(8000, rh=20) > air_absorption(8000, rh=70)


def test_double_distance_loses_6_db():
    assert level_at(90, 2) - level_at(90, 4) == pytest.approx(6.02, abs=0.01)


def test_air_adds_to_spreading():
    assert level_at(90, 100, freq=8000) < level_at(90, 100)
    assert level_at(90, 1, freq=8000) == pytest.approx(90)
