import json
from enum import Enum

from flask_sqlalchemy import SQLAlchemy
from work_timer_back.app import app
from work_timer_back.json import ToJSONMixin
from work_timer_back.utils import tz_aware_now

db = SQLAlchemy(app)


class TableNames(Enum):
    category = "categories"
    events = "events"


class Event(db.Model, ToJSONMixin):
    __tablename__ = TableNames.events.value

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(
        db.DateTime(timezone=True), default=tz_aware_now, nullable=False
    )

    start = db.Column(
        db.DateTime(timezone=True), default=tz_aware_now, nullable=False
    )
    end = db.Column(db.DateTime(timezone=True), nullable=True)

    category_id = db.Column(
        db.Integer,
        db.ForeignKey(f"{TableNames.category.value}.id"),
        nullable=False,
    )
    category = db.relationship("Category", back_populates="events")

    def to_json(self):
        end = self.end.isoformat() if self.end else None

        return {
            "id": self.id,
            "created": self.created.isoformat(),
            "start": self.start.isoformat(),
            "end": end,
            "category_id": self.category_id,
        }


class Category(db.Model, ToJSONMixin):
    __tablename__ = TableNames.category.value

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True), default=tz_aware_now)

    name = db.Column(db.Text, nullable=False)

    events = db.relationship("Event", back_populates="category")

    def to_json(self):
        return {
            "id": self.id,
            "created": self.created.isoformat(),
            "name": self.name,
        }
