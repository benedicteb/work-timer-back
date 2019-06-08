from functools import wraps

from flask import abort, request

_SECRET_KEY = "abc123"


def authenticated():
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return abort(401)

            try:
                method, token = auth_header.strip().split()
            except ValueError:
                return abort(401)

            if method != "Bearer" or token != _SECRET_KEY:
                return abort(401)

            return f(*args, **kwargs)

        return wrapped

    return decorator
