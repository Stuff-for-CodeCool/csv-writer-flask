from flask import Flask, render_template, request, redirect, url_for, flash
from data import read_all_entries, insert_entry, read_entry

app = Flask(__name__)
app.secret_key = "alskua ekjegu keucyf iqek,rvgkfarg rkjegkjqaved"


@app.route("/")
def index():
    entries = read_all_entries()
    return render_template("index.html", entries=entries)


@app.route("/entry/<int:id>")
def get_entry(id):
    entry = read_entry(id)

    title = entry["title"]
    message = entry["message"]
    view_count = entry["view_count"]

    return render_template(
        "entry.html",
        title=title,
        message=message,
        view_count=view_count,
    )


@app.route("/add", methods=["POST"])
def adding():
    title = request.form.get("title")
    message = request.form.get("message")

    if insert_entry(title, message):
        flash("Entry added")
        return redirect(url_for("index"))

    flash("Entry not added")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
