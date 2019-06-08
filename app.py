import os

import work_timer_back.views
from work_timer_back.app import app
from work_timer_back.models import db

if __name__ == "__main__":
    db_host = os.getenv("DB_HOST", "0.0.0.0")
    db_user = os.getenv("DB_USER", "dbuser")
    db_password = os.getenv("DB_PASSWORD", "abc123")
    db_name = os.getenv("DB_NAME", "work_timer_db")

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
    app.config["AUTHORIZATION_KEY"] = os.getenv("AUTHORIZATION_KEY", "abc123")

    host = os.getenv("FLASK_HOST", "localhost")
    port = os.getenv("FLASK_PORT", "5000")
    debug = os.getenv("FLASK_ENVIRONMENT", "development") == "development"

    db.create_all()

    app.run(host=host, port=port, debug=debug)
