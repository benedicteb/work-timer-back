from flask import Flask
from work_timer_back.json import ToJSONEncoder

app = Flask("work-timer-back")

app.json_encoder = ToJSONEncoder
