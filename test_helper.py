import pytest
import helper
import datetime


def test_add():
    helper.items.clear()
    text = "Lorem ipsum"
    date = "2023-09-02"
    helper.add(text=text, date_str=date)
    item = helper.items[-1]
    assert isinstance(item.date, datetime.date)


def test_sort():
    helper.items.clear()
    todos = [
        ("Universum debuggen", "2023-09-06"),
        ("Sinn des Lebens entdecken", "2023-09-01"),
        ("Superheld werden", "2023-10-25"),
        ("Netto null", "2050-01-01"),
    ]

    for text, date in todos:
        helper.add(text=text, date_str=date)

    for i in range(len(helper.items) - 1):
        assert helper.items[i].date < helper.items[i + 1].date


def test_add_with_description():
    helper.items.clear()
    text = "Testaufgabe mit Beschreibung"
    date = "2025-12-24"
    description = "Dies ist die Beschreibung"

    helper.add(text=text, date_str=date, description=description)
    item = helper.items[-1]
    assert item.description == description

def test_add_with_category():
    helper.items.clear()
    text = "Testaufgabe mit Kategorie"
    date = "2025-01-01"
    category = "Arbeit"
    helper.add(text=text, date_str=date, category=category)
    item = helper.items[-1]
    assert item.category == category
