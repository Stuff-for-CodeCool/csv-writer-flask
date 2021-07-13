from flask import Flask, render_template, request, redirect, url_for, flash
import data

app = Flask(__name__)
app.secret_key = "iuhksdhvlksjhlkfsafvlksfhkj"

PAGES_START_AT = 1
POSTS_PER_PAGE = 20


@app.route("/")
@app.route("/page/<int:page>")
@app.route("/page/<int:page>/")
def index(page=(PAGES_START_AT - 1)):
    entries = data.read_all_entries(start_at=page, limit=POSTS_PER_PAGE)
    prev = (page - 1) if page > 0 else None
    next = (page + 1) if page < data.count_entries() // POSTS_PER_PAGE else None

    return render_template(
        "index.html",
        entries=entries,
        page=page,
        prev=prev,
        next=next,
    )


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
