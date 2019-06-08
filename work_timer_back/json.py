from functools import wraps

from flask import Response, abort, jsonify, request
from flask.json import JSONEncoder


class ToJSONEncoder(JSONEncoder):
    def default(self, o):
        try:
            return o.to_json()
        except AttributeError:
            return super().default(o)


class ToJSONMixin:
    def to_json(self):
        raise NotImplementedError()


def parse_json_body(field_names):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            body = request.json

            if not body:
                return abort(400)

            for field_name in field_names:
                if body.get(field_name) is None:
                    response = jsonify(
                        {"message": f"Field '{field_name}' missing"}
                    )
                    response.status_code = 400

                    return abort(response)

            return f(body, *args, **kwargs)

        return wrapped

    return decorator
