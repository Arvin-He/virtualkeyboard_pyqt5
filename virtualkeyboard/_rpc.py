# -*- coding:utf-8 -*-
import ast
import gevent.socket

_SERVER_ADDRESS = ("127.0.0.1", 21000)


class _Connection:
    _pool = []

    def __init__(self):
        self._socket = gevent.socket.socket(
            gevent.socket.AF_INET, gevent.socket.SOCK_DGRAM)
        self._socket.connect(_SERVER_ADDRESS)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self._pool.append(self)

    @classmethod
    def get(cls):
        return cls._pool.pop() if cls._pool else cls()

    def request(self, data):
        self._socket.send(data)
        return self._socket.recv(65536)


def _eval(script, timeout=5):
    with _Connection.get() as connection:
        with gevent.Timeout(timeout):
            result = connection.request(b"EVAL\n" + script.encode())
    if not result.startswith(b"OK\n"):
        if result.startswith(b"ERROR\n"):
            result = result[6:].decode()
        raise RuntimeError(result)
    return ast.literal_eval(result[3:].decode())


def _exec(script, timeout=5):
    with _Connection.get() as connection:
        with gevent.Timeout(timeout):
            result = connection.request(b"EXEC\n" + script.encode())
    if result != b"OK":
        if result.startswith(b"ERROR\n"):
            result = result[6:].decode()
        raise RuntimeError(result)
