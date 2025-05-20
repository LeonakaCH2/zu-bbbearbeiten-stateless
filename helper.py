from dataclasses import dataclass
import datetime
import csv
import io


items = []


@dataclass
class Item:
    text: str
    date: datetime.date
    category: str = ""
    description: str = ""
    isCompleted: bool = False


def add(text, date_str=None, category="", description=""):
    if date_str is None:
        raise ValueError("Date is required")

    if isinstance(date_str, str):
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    elif isinstance(date_str, datetime.date):
        date = date_str
    else:
        raise ValueError("Date must be a string or datetime.date")

    text = text.replace("b", "bbb").replace("B", "Bbb")
    items.append(Item(text=text, date=date, category=category, description=description))
    items.sort(key=lambda item: item.date)


def get_all():
    return items


def get(index):
    return items[index]


def update(index):
    items[index].isCompleted = not items[index].isCompleted


def get_csv():
    output = io.StringIO()
    writer = csv.writer(output)

    # Kopfzeile
    writer.writerow(["text", "category", "date", "description", "isCompleted"])

    for item in items:
        writer.writerow(
            [
                item.text,
                item.category,
                item.date.strftime("%Y-%m-%d"),
                item.description,
                item.isCompleted,
            ]
        )

    return output.getvalue()
