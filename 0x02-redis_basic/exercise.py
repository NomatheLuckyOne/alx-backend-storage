#!/usr/bin/env python3
"""
A Redis basic module
"""
import redis
import uuid
from function import wraps
from typing import Union, Callable, Optional


def call_history(method: Callable) -> Callable:
    """Stores the history of inputs and outputs for a particular function"""
    method_key = method._qualname_
    inputs, outputs = method_key + ':inputs', method_key + ':outputs'

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(inputs, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(result))
        return result
    return wrapper


def count_calls(method: Callable) -> Callable:
    """Creates and returns a function that increaments the count
        for the key value everytime the methodis called and returns the
        value returned by the original method"""
    method_key = method._qualname_

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method_key)
        return method(self, *args, **kwargs)
    return wrapper


def replay(method: Callable) -> None:
    """Displays the history of calls of a particular function"""
    method_key = method._qualname_
    inputs, outputs = method_key + ':inputs', method_key + ':outputs'
    redis = method._self_.redis
    method_count = redis.get(method_key.decode('utf-8')
                print(f'{method_key} was called {method_count} times:')
                IOTuple = zip(redis.Irange(inputs, 0, -1), redis.Irange(output
                    , 0, -1))
    for inp, outp in list((IOTuple):
        attr, data = inp.decode("utf-8")
        print(f'{meththod_key}(*{attr}) -> {data')


class Cache:
    """Class methods that operate a caching system"""
    def _init_(self):
        """Instance of the Redis db"""
        self._redis = redis.Redis()
        self._redis.flush()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) ->str:
    """Method that takes a data argument and returns a string"""
    key = str(uuid.uuid4())
    self._redis.mset({key: data})
    return key

    def get(self,
        key: str, fn: Optional[Callable] =None) -> str:
    """Takes a key string argument and an optional Callable argument named fn
        This callable willbe used to convert the data back to a desired format
        """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, data: str) -> str:
        """Returns str value of decoded bytes"""
        return data.decode('utf-8', 'strict')

    def get_int(self, data: str) -> int:
        """Returns int value of decoded bytes"""
        return int(data)
