import pytest
import helper
import datetime
from flask import Flask


@pytest.fixture(scope="session", autouse=True)
def init_db():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo_test.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.app_context().push()
    helper.db.init_app(app)
    helper.db.create_all()
    yield
    helper.db.session.remove()
    helper.db.drop_all()


def clear_db():
    helper.db.session.query(helper.Item).delete()
    helper.db.session.commit()


def test_add():
    clear_db()
    text = "Lorem ipsum"
    date = "2023-09-02"
    helper.add(text=text, date_str=date)
    item = helper.get_all()[-1]
    assert isinstance(item.date, datetime.date)


def test_sort():
    clear_db()
    todos = [
        ("Universum debuggen", "2023-09-06"),
        ("Sinn des Lebens entdecken", "2023-09-01"),
        ("Superheld werden", "2023-10-25"),
        ("Netto null", "2050-01-01"),
    ]

    for text, date in todos:
        helper.add(text=text, date_str=date)

    items = helper.get_all()
    for i in range(len(items) - 1):
        assert items[i].date <= items[i + 1].date


def test_add_with_description():
    clear_db()
    text = "Testaufgabe mit Beschreibung"
    date = "2025-12-24"
    description = "Dies ist die Beschreibung"

    helper.add(text=text, date_str=date, description=description)
    item = helper.get_all()[-1]
    assert item.description == description


def test_add_with_category():
    clear_db()
    text = "Testaufgabe mit Kategorie"
    date = "2025-01-01"
    category = "Arbeit"
    helper.add(text=text, date_str=date, category=category)
    item = helper.get_all()[-1]
    assert item.category == category


def test_get_csv():
    clear_db()
    helper.add(
        text="Mathe lernen",
        date_str="2025-06-01",
        category="Schule",
        description="Algebra, Geometrie",
    )
    csv = helper.get_csv()

    # CSV sollte Kopfzeile + eine Zeile haben
    lines = csv.strip().splitlines()
    assert lines[0] == "text,category,date,description,isCompleted"
    assert "Mathe lernen" in lines[1]
    assert "Schule" in lines[1]
    assert "Algebra, Geometrie" in lines[1]
