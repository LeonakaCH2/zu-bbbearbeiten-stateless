from dataclasses import dataclass
import datetime


items = []


@dataclass
class Item:
    text: str
    date: datetime.date
    isCompleted: bool = False


def add(text, date_str):

    if isinstance(date_str, str):
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    elif isinstance(date_str, datetime.date):
        date = date_str
    else:
        raise ValueError("Date must be a string or datetime.date")

    text = text.replace('b', 'bbb').replace('B', 'Bbb')
    items.append(Item(text=text, date=date))


def get_all():
    return items


def get(index):
    return items[index]


def update(index):
    items[index].isCompleted = not items[index].isCompleted
