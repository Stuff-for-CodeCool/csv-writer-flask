from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
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
    entries = [
        dict(
            link=url_for("get_entry", id=e.get("id")),
            title=e.get("title"),
            message=e.get("message"),
            view_count=e.get("view_count"),
        )
        for e in entries
    ]

    prev = url_for("index", page=(page - 1)) if page > 1 else None
    next = (
        url_for("index", page=(page + 1))
        if page < (data.count_all_entries() // POSTS_PER_PAGE)
        else None
    )

    if request.is_json:
        return jsonify(
            dict(
                entries=entries,
                page=page,
                prev=prev,
                next=next,
            )
        )

    return render_template(
        "index.html",
        entries=entries,
        page=page,
        prev=prev,
        next=next,
    )


@app.route("/entry/<int:id>")
@app.route("/entry/<int:id>/")
def get_entry(id, as_json=False):
    try:
        (id, title, message, view_count) = data.get_entry(id).values()

        if request.is_json or as_json:
            return jsonify(
                dict(
                    title=title,
                    message=message,
                    view_count=view_count,
                )
            )

        return render_template(
            "entry.html",
            title=title,
            message=message,
            view_count=view_count,
        )
    except AttributeError:
        if request.is_json:
            return jsonify(
                dict(error="You have tried to reach a page that doesn't exist")
            )

        return page_not_found()


@app.route("/add", methods=["POST"])
@app.route("/add/", methods=["POST"])
def add_entry():
    title = (
        request.json.get("title", None)
        if request.is_json
        else request.form.get("title", None)
    )
    message = (
        request.json.get("message", None)
        if request.is_json
        else request.form.get("message", None)
    )

    if not title or not message:
        flash("Please fill in all required fields")
    else:
        id = data.add_entry(title=title, message=message)

        if request.is_json:
            return get_entry(id, True)

        return redirect(url_for("get_entry", id=id))

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
