from flask import jsonify, request
from work_timer_back.app import app
from work_timer_back.auth import authenticated
from work_timer_back.json import parse_json_body
from work_timer_back.models import Category, db


@app.route("/", methods=["GET"])
def hello_world():
    return jsonify({"hello": True})


@app.route("/category", methods=["POST"])
@authenticated()
@parse_json_body(["categoryName"])
def create_category(json):
    category_name = json["categoryName"]

    new_category = Category(name=category_name)

    db.session.add(new_category)
    db.session.commit()

    return jsonify(new_category)
