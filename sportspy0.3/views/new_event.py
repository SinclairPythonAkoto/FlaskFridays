from flask import Blueprint, render_template, url_for, request


new_event = Blueprint(
    "new_event",
    __name__,
    static_folder="static",
    template_folder="templates",
)


@new_event.route("/newEvent", methods=["GET", "POST"])
def new_project():
    if request.method == "GET":
        return render_template("newEvent.html")
    else:
        return render_template("newEvent.html")