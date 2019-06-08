from flask import Flask
from work_timer_back.json import ToJSONEncoder

app = Flask("work-timer-back")

app.json_encoder = ToJSONEncoder


@app.after_request
def apply_caching(response):
    response.headers[
        "Access-Control-Allow-Origin"
    ] = "https://work-timer.benedicte.dev"

    response.headers["Access-Control-Allow-Methods"] = ", ".join(
        ["GET", "POST", "PUT", "OPTIONS"]
    )

    response.headers["Access-Control-Allow-Headers"] = ", ".join(
        ["Authorization", "Content-Type"]
    )

    return response
