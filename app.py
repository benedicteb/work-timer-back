import os

import work_timer_back.views
from work_timer_back.app import app
from work_timer_back.models import db

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///work_timer.sqlite"

host = os.getenv("FLASK_HOST", "localhost")
port = os.getenv("FLASK_PORT", "5000")
debug = os.getenv("FLASK_ENVIRONMENT", "development") == "development"

db.create_all()

app.run(host=host, port=port, debug=debug)
