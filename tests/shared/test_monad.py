import pytest

from shared.monad import Result


pytestmark = pytest.mark.unit


# ─── Success ──────────────────────────────────────────────────────────────────


def test_success_is_ok():
    result = Result.Success(42)
    assert result.is_ok() is True


def test_success_holds_value():
    result = Result.Success("hello")
    assert result.value() == "hello"


def test_success_with_none_value():
    result = Result.Success(None)
    assert result.is_ok() is True
    assert result.value() is None


# ─── Failure ──────────────────────────────────────────────────────────────────


def test_failure_is_not_ok():
    result = Result.Failure("something went wrong")
    assert result.is_ok() is False


def test_failure_holds_error():
    error = ValueError("bad input")
    result = Result.Failure(error)
    assert result.value() is error


# ─── bind ─────────────────────────────────────────────────────────────────────


def test_bind_transforms_success_value():
    result = Result.Success(5).bind(lambda x: Result.Success(x * 2))
    assert result.is_ok() is True
    assert result.value() == 10


def test_bind_short_circuits_on_failure():
    called = []
    result = Result.Failure("err").bind(lambda x: called.append(x) or Result.Success(x))
    assert result.is_ok() is False
    assert called == []


def test_bind_propagates_failure_through_chain():
    result = (
        Result.Success(10)
        .bind(lambda x: Result.Success(x + 1))
        .bind(lambda _: Result.Failure("abort"))
        .bind(lambda x: Result.Success(x * 100))
    )
    assert result.is_ok() is False
    assert result.value() == "abort"


def test_bind_chains_multiple_successful_steps():
    result = (
        Result.Success(1)
        .bind(lambda x: Result.Success(x + 1))
        .bind(lambda x: Result.Success(x * 10))
        .bind(lambda x: Result.Success(f"value={x}"))
    )
    assert result.is_ok() is True
    assert result.value() == "value=20"


def test_bind_success_to_failure_stops_at_failure():
    steps = []

    def step(label):
        def _fn(x):
            steps.append(label)
            return Result.Success(x) if label != "bad" else Result.Failure("stopped")

        return _fn

    result = Result.Success(0).bind(step("a")).bind(step("bad")).bind(step("c"))
    assert result.is_ok() is False
    assert "c" not in steps
