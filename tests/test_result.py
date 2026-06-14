from __future__ import annotations

from decimal import Decimal

import pytest

from src.application.result import Result


def test_success_result():
    r = Result.success(42)
    assert r.is_success
    assert not r.is_failure
    assert r.unwrap() == 42


def test_failure_result():
    r = Result.failure("error")
    assert r.is_failure
    assert not r.is_success
    assert r.unwrap_error() == "error"


def test_result_cannot_have_both():
    with pytest.raises(ValueError):
        Result(value=1, error="e")


def test_result_must_have_one():
    with pytest.raises(ValueError):
        Result(value=None, error=None)


def test_map_success():
    r = Result.success(2).map(lambda x: x * 3)
    assert r.unwrap() == 6


def test_map_failure():
    r = Result.failure("err").map(lambda x: x * 3)
    assert r.is_failure
    assert r.unwrap_error() == "err"
