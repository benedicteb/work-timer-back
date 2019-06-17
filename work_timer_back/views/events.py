import logging
from enum import Enum

import dateutil
import dateutil.parser

from flask import abort, jsonify, request
from work_timer_back.app import app
from work_timer_back.auth import authenticated
from work_timer_back.json import parse_json_body
from work_timer_back.utils import tz_aware_now
from work_timer_back.models import Event, Category, db

_LOG = logging.getLogger(__name__)


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


@app.route("/event/<event_id>/stop", methods=["POST"])
@authenticated()
def stop_event(event_id):
    event = db.session.query(Event).get(event_id)

    if not event:
        return abort(400)

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
        return abort(400)

    return jsonify(event)


@app.route("/event/<event_id>", methods=["DELETE"])
@authenticated()
def delete_event(event_id):
    event = db.session.query(Event).get(event_id)

    if not event:
        return abort(400)

    db.session.remove(event)
    db.session.commit()

    return jsonify({"deleted": event_id})


@app.route("/event/<event_id>", methods=["PUT"])
@authenticated()
@parse_json_body()
def edit_event(json, event_id):
    event = db.session.query(Event).get(event_id)

    if not event:
        return abort(400)

    keys = json.keys()

    if "start" in keys:
        try:
            start = dateutil.parser.parse(json["start"])
        except ValueError:
            return abort(400)

        event.start = start

    if "end" in keys:
        try:
            end = dateutil.parser.parse(json["end"])
        except ValueError:
            return abort(400)

        event.end = end

    if "categoryId" in keys:
        category = db.session.query(Category).get(json["categoryId"])

        if not category:
            return abort(400)

        event.category = category

    db.session.commit()

    return jsonify(event)


@app.route("/events", methods=["GET"])
@authenticated()
def get_events():
    query = db.session.query(Event)
    query_params = request.args

    class QueryParams(Enum):
        after = "after"
        before = "before"
        running = "running"

    if QueryParams.after.value in query_params.keys():
        try:
            after = dateutil.parser.parse(
                query_params[QueryParams.after.value]
            )
        except ValueError:
            return abort(400)

        query = query.filter(Event.start > after)

    if QueryParams.before.value in query_params.keys():
        try:
            before = dateutil.parser.parse(
                query_params[QueryParams.before.value]
            )
        except ValueError:
            return abort(400)

        query = query.filter(Event.start < before)

    if QueryParams.running.value in query_params.keys():
        if query_params[QueryParams.running.value] == "1":
            query = query.filter(Event.end == None)

    return jsonify({"events": query.all()})
