from sys import path
from pathlib import Path

from numpy import var
homedir = Path(__file__).parent.parent
print(homedir)
path.append(f"{homedir}/src/omilia_telnum")

from modules import (
    validate_phone, is_phone_number, _check_0space_variances,
    _check_2digits_variances, check_ambiguities
    )

import pytest

def test_validate_phone():
    assert validate_phone("2101234567") == True
    assert validate_phone("21012345678") == False
    assert validate_phone("00302101234567") == True
    assert validate_phone("6912345678") == True
    assert validate_phone("00306912345678") == True
    assert validate_phone("1234567890") == False
    assert validate_phone("00301234567890") == False
    assert validate_phone(2101234567) == True
    assert validate_phone(21012345678) == False
    assert validate_phone(6912345678) == True
    assert validate_phone(1234567890) == False
    assert validate_phone(None) == False
    assert validate_phone("abcdefghij") == False
    assert validate_phone("") == False

def test_validate_phone_invalid_types():
    assert is_phone_number("21 01 23 45 67") == True
    assert is_phone_number("01234567") == True
    assert is_phone_number(2101234567) == True
    assert is_phone_number(12.34) == False
    assert is_phone_number(None) == False
    assert is_phone_number(True) == False

def test_check_0space_variances():

    variants = _check_0space_variances("1 2 30 4 5 60 7 8 9")
    expected_variants = [
        "1 2 30 4 5 60 7 8 9",
        "1 2 3 4 5 60 7 8 9",
        "1 2 30 4 5 6 7 8 9",
        "1 2 3 4 5 6 7 8 9"
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
    expected_variants = [
        "1 2 30 45 6 7 8 9"
        ]
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
        "0030 69 1 2 3 405 6 7 8"
    ]
    for variant in variants:
        assert variant in expected_variants
    assert len(variants) == len(expected_variants)
    
    variants = check_ambiguities("69 1 2 3 4 5 6 7 8")
    expected_variants = ["69 1 2 3 4 5 6 7 8"]
    for variant in variants:
        assert variant in expected_variants
    assert len(variants) == len(expected_variants)
