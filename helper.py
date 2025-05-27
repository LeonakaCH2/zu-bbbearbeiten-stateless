from dataclasses import dataclass
import datetime
import csv
import io
from flask_sqlalchemy import SQLAlchemy
from database import db


@dataclass
class Item(db.Model):
    id: int
    text: str
    date: datetime.date
    category: str
    description: str
    isCompleted: bool

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    date = db.Column(db.Date)
    category = db.Column(db.String)
    description = db.Column(db.String)
    isCompleted = db.Column(db.Boolean, default=False)


def add(text, date_str=None, category="", description=""):
    if not date_str:
        raise ValueError("Date is required")

    if isinstance(date_str, str):
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    elif isinstance(date_str, datetime.date):
        date = date_str
    else:
        raise ValueError("Date must be a string or datetime.date")

    # Text-Transformation beibehalten
    text = text.replace("b", "bbb").replace("B", "Bbb")

    item = Item(
        text=text,
        date=date,
        category=category,
        description=description,
        isCompleted=False,
    )

    db.session.add(item)
    db.session.commit()


def get_all():
    return Item.query.order_by(Item.date.asc(), Item.category.desc()).all()


def get(item_id):
    return db.session.query(Item).get(item_id)


def update(item_id):
    item = db.session.query(Item).get(item_id)
    if item:
        item.isCompleted = not item.isCompleted
        db.session.commit()


def get_csv():
    output = io.StringIO()
    writer = csv.writer(output)

    # Kopfzeile
    writer.writerow(["text", "category", "date", "description", "isCompleted"])

    for item in Item.query.order_by(Item.date.asc()).all():
        writer.writerow(
            [
                item.text,
                item.category,
                item.date.strftime("%d.%m.%Y"),
                item.description,
                item.isCompleted,
            ]
        )

    return output.getvalue()
