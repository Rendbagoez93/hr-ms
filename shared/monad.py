from collections.abc import Callable
from typing import Any, TypeVar


T = TypeVar("T")  # Success type
E = TypeVar("E")  # Error type


class Result[T, E]:
    def __init__(self, value: T | E, is_success: bool):  # noqa: FBT001
        self._value = value
        self._is_success = is_success

    @classmethod
    def Success(cls, value: T) -> Result[T, E]:  # noqa: N802
        return cls(value, True)  # noqa: FBT003

    @classmethod
    def Failure(cls, error: E) -> Result[T, E]:  # noqa: N802
        return cls(error, False)  # noqa: FBT003

    def bind(self, func: Callable[[T], Result[Any, E]]) -> Result[Any, E]:
        """The core Monad 'pipe'. If this is a failure, skip the function."""
        if not self._is_success:
            return self
        return func(self._value)

    def is_ok(self) -> bool:
        return self._is_success

    def value(self) -> T:
        return self._value

    def error(self) -> E:
        return self._value
