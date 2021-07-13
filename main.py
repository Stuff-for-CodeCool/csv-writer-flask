from flask import Flask, render_template, request, redirect, url_for, flash
import data

app = Flask(__name__)
app.secret_key = "iuhksdhvlksjhlkfsafvlksfhkj"


@app.errorhandler(404)
def page_not_found():
    return render_template("404.html")


POSTS_PER_PAGE = 4


@app.route("/")
@app.route("/page/<int:page>")
@app.route("/page/<int:page>/")
def index(page=1):
    entries = data.get_paged_entries(
        page=page,
        limit=POSTS_PER_PAGE,
    )

    prev = page - 1 if page > 1 else None
    next = page + 1 if page < (data.count_all_entries() // POSTS_PER_PAGE) else None

    return render_template(
        "index.html",
        entries=entries,
        page=page,
        prev=prev,
        next=next,
    )


@app.route("/entry/<int:id>")
@app.route("/entry/<int:id>/")
def get_entry(id):
    try:
        (id, title, message, view_count) = data.get_entry(id).values()

        return render_template(
            "entry.html",
            title=title,
            message=message,
            view_count=view_count,
        )
    except AttributeError:
        return page_not_found()


@app.route("/add", methods=["POST"])
@app.route("/add/", methods=["POST"])
def add_entry():
    title = request.form.get("title", None)
    message = request.form.get("message", None)

    if not title or not message:
        flash("Please fill in all required fields")
    else:
        id = data.add_entry(title=title, message=message)
        return redirect(url_for("get_entry", id=id))

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
