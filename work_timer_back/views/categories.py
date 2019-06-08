from flask import jsonify
from work_timer_back.app import app
from work_timer_back.auth import authenticated
from work_timer_back.json import require_json_fields
from work_timer_back.models import Category, db


@app.route("/category", methods=["POST"])
@authenticated()
@require_json_fields(["categoryName"])
def create_category(json):
    category_name = json["categoryName"]

    new_category = Category(name=category_name)

    db.session.add(new_category)
    db.session.commit()

    return jsonify(new_category)
