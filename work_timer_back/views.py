import dateutil
import dateutil.parser

from flask import abort, jsonify, request
from work_timer_back.app import app
from work_timer_back.auth import authenticated
from work_timer_back.json import parse_json_body, require_json_fields
from work_timer_back.utils import tz_aware_now
from work_timer_back.models import Event, Category, db


@app.route("/", methods=["GET"])
def hello_world():
    return jsonify({"hello": True})


@app.route("/category", methods=["POST"])
@authenticated()
@require_json_fields(["categoryName"])
def create_category(json):
    category_name = json["categoryName"]

    new_category = Category(name=category_name)

    db.session.add(new_category)
    db.session.commit()

    return jsonify(new_category)


@app.route("/category/<category_id>/event", methods=["POST"])
@authenticated()
@parse_json_body()
def create_event(json, category_id):
    category = db.session.query(Category).get(category_id)

    if not category:
        return abort(400)

    new_event = Event(category=category)

    if json.get("start") is not None:
        try:
            start = dateutil.parser.parse(json["start"])
        except ValueError:
            return abort(400)

        new_event.start = start
    else:
        new_event.start = tz_aware_now()

    if json.get("end") is not None:
        try:
            end = dateutil.parser.parse(json["end"])
        except ValueError:
            return abort(400)

        if end < new_event.start:
            return abort(400)

        new_event.end = end

    db.session.add(new_event)
    db.session.commit()

    return jsonify(new_event)


@app.route("/category/<category_id>/start", methods=["POST"])
@authenticated()
def start_event(category_id):
    category = db.session.query(Category).get(category_id)

    if not category:
        return abort(400)

    new_event = Event(category=category)

    db.session.add(new_event)
    db.session.commit()

    return jsonify(new_event)


@app.route("/event/<event_id>/stop", methods=["POST"])
@authenticated()
def stop_event(event_id):
    event = db.session.query(Event).get(event_id)

    if not event:
        return abort(404)

    if event.end is not None:
        return abort(400)

    event.end = tz_aware_now()

    db.session.commit()

    return jsonify(event)


@app.route("/event/<event_id>", methods=["GET"])
@authenticated()
def get_event(event_id):
    event = db.session.query(Event).get(event_id)

    if not event:
        return abort(404)

    return jsonify(event)
