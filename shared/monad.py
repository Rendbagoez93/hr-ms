from typing import Generic, TypeVar, Callable, Any, Union

T = TypeVar('T')  # Success type
E = TypeVar('E')  # Error type

class Result(Generic[T, E]):
    def __init__(self, value: Union[T, E], is_success: bool):
        self._value = value
        self._is_success = is_success

    @classmethod
    def Success(cls, value: T) -> 'Result[T, E]':
        return cls(value, True)

    @classmethod
    def Failure(cls, error: E) -> 'Result[T, E]':
        return cls(error, False)

    def bind(self, func: Callable[[T], 'Result[Any, E]']) -> 'Result[Any, E]':
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
    
    