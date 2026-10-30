from pathlib import Path
from sys import path

import pytest

homedir = Path(__file__).parent.parent
print(homedir)
path.append(f"{homedir}/src/natural-numbers-interpretation")

from modules import (
    _check_0space_variances,
    _check_2digits_variances,
    check_ambiguities,
    is_phone_number,
    validate_phone,
)


def test_validate_phone():
    assert validate_phone("2101234567")
    assert not validate_phone("21012345678")
    assert validate_phone("00302101234567")
    assert validate_phone("6912345678")
    assert validate_phone("00306912345678")
    assert not validate_phone("1234567890")
    assert not validate_phone("00301234567890")
    assert validate_phone(2101234567)
    assert not validate_phone(21012345678)
    assert validate_phone(6912345678)
    assert not validate_phone(1234567890)
    assert not validate_phone(None)
    assert not validate_phone("abcdefghij")
    assert not validate_phone("")


def test_validate_phone_invalid_types():
    assert is_phone_number("21 01 23 45 67")
    assert is_phone_number("01234567")
    assert is_phone_number(2101234567)
    assert not is_phone_number(12.34)
    assert not is_phone_number(None)
    assert not is_phone_number(True)


def test_check_0space_variances():

    variants = _check_0space_variances("1 2 30 4 5 60 7 8 9")
    expected_variants = [
        "1 2 30 4 5 60 7 8 9",
        "1 2 3 4 5 60 7 8 9",
        "1 2 30 4 5 6 7 8 9",
        "1 2 3 4 5 6 7 8 9",
    ]
    for variant in variants:
        print(f"Variant: {variant}")
        assert variant in expected_variants
    assert len(variants) == len(expected_variants)

    variants = _check_0space_variances("0 1 2 3 4 5 6 7 8 9")
    expected_variants = ["0 1 2 3 4 5 6 7 8 9"]
    for variant in variants:
        assert variant in expected_variants
    assert len(variants) == len(expected_variants)

    variants = _check_0space_variances("1 2 30 45 6 7 8 9")
    expected_variants = ["1 2 30 45 6 7 8 9"]
    for variant in variants:
        assert variant in expected_variants
    assert len(variants) == len(expected_variants)


def test_check_0space_variances_invalid_types():

    pytest.raises(TypeError, _check_0space_variances, None)
    pytest.raises(TypeError, _check_0space_variances, 12.5)


def test_check_2digits_variances():

    variants = _check_2digits_variances("1 23 4")
    expected_variants = ["1 23 4", "1 203 4"]
    for variant in variants:
        assert variant in expected_variants
    assert len(variants) == len(expected_variants)

    variants = _check_2digits_variances("1 2 4")
    expected_variants = ["1 2 4"]
    for variant in variants:
        assert variant in expected_variants
    assert len(variants) == len(expected_variants)


def test_check_2digits_variances_invalid_types():

    pytest.raises(TypeError, _check_2digits_variances, None)
    pytest.raises(TypeError, _check_2digits_variances, 12.5)


def test_check_ambiguities():

    variants = check_ambiguities("0030 69 10 2 3 45 6 7 8")
    expected_variants = [
        "0030 69 10 2 3 45 6 7 8",
        "0030 69 1 2 3 45 6 7 8",
        "0030 69 10 2 3 405 6 7 8",
        "0030 69 1 2 3 405 6 7 8",
    ]
    for variant in variants:
        assert variant in expected_variants
    assert len(variants) == len(expected_variants)

    variants = check_ambiguities("69 1 2 3 4 5 6 7 8")
    expected_variants = ["69 1 2 3 4 5 6 7 8"]
    for variant in variants:
        assert variant in expected_variants
    assert len(variants) == len(expected_variants)
