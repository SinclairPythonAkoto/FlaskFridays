from flask import Flask 
from flask import render_template, url_for

app = Flask(__name__)

@app.route("/")
def landingpage():
    return render_template("landingPage.html")

@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

@app.route("/writeReview")
def writeReview():
    return render_template('writeReviewPage.html')

@app.route('/viewReviews')
def view_reviews():
    return render_template('searchReviewPage.html')

if __name__ == "__main__":
    app.run(debug=True)