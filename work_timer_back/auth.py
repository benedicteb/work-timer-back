from functools import wraps

from flask import abort, request
from work_timer_back.app import app


def authenticated():
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            secret_key = app.config["AUTHORIZATION_KEY"]
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return abort(401)

            try:
                method, token = auth_header.strip().split()
            except ValueError:
                return abort(401)

            if method != "Bearer" or token != secret_key:
                return abort(401)

            return f(*args, **kwargs)

        return wrapped

    return decorator
