from flask import abort, jsonify
from work_timer_back.app import app
from work_timer_back.auth import authenticated
from work_timer_back.json import require_json_fields
from work_timer_back.utils import tz_aware_now
from work_timer_back.models import Event, Category, db


@app.route("/category", methods=["POST"])
@authenticated()
@require_json_fields(["categoryName"])
def create_category(json):
    category_name = json["categoryName"]

    new_category = Category(name=category_name)

    db.session.add(new_category)
    db.session.commit()

    return jsonify(new_category)


@app.route("/category/<category_id>/start", methods=["POST"])
@authenticated()
def start_category_event(category_id):
    category = db.session.query(Category).get(category_id)

    if not category:
        return abort(400)

    new_event = Event(category=category)

    db.session.add(new_event)
    db.session.commit()

    return jsonify(new_event)


@app.route("/category/<category_id>/stop", methods=["POST"])
@authenticated()
def stop_category_events(category_id):
    category = db.session.query(Category).get(category_id)

    if not category:
        return abort(400)

    events_to_stop = db.session.query(Event).filter(Event.end == None).all()
    ids_stopped = []
    now = tz_aware_now()

    for event in events_to_stop:
        event.end = now
        ids_stopped.append(event.id)

    db.session.commit()

    return jsonify(ids_stopped)
