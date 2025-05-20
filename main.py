import helper
from flask import Flask, request, Response, render_template, redirect, url_for

app = Flask(__name__)


@app.route("/")
def index():
    items = helper.get_all()
    return render_template("index.html", items=items)


@app.route("/add", methods=["POST"])
def add():
    text = request.form.get("text")
    date_str = request.form.get("date")
    description = request.form.get("description")  # 🆕 aus dem Formular lesen
    helper.add(text=text, date_str=date_str, description=description)  # 🆕 übergeben
    return redirect(url_for("index"))


@app.route("/update/<int:index>")
def update(index):
    helper.update(index)
    return redirect(url_for("index"))
