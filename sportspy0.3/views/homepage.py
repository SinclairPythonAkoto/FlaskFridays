from flask import Blueprint, render_template, url_for


homepage = Blueprint(
    "homepage",
    __name__,
    static_folder="static",
    template_folder="templates",
)

@homepage.route("/home")
def home_page():
    return render_template("homepage.html")