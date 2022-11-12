from flask import Blueprint, render_template


hello = Blueprint(
    "hello",
    __name__,
    static_folder="static",
    template_folder="templates",
)


@hello.route("/")
def hello_world():
    return render_template("landingpage.html")