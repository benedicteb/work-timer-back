from flask import jsonify, request
from work_timer_back.app import app
from work_timer_back.auth import authenticated


@app.route("/", methods=["GET"])
def hello_world():
    return jsonify({"hello": True})


@app.route("/category", methods=["POST"])
@authenticated()
def create_category():
    return jsonify({"result": True})
