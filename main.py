from flask import Flask, request, render_template, redirect, url_for
from schedule import get_calendar
from populate import populate

calendar = []

# Run flask
app = Flask(__name__)

@app.route("/", methods = ["POST", "GET"])
def index():
    global calendar
    if request.method == "POST":
        calendar = get_calendar().items()
        populate(calendar)
        return redirect(url_for("success"))
    return render_template("index.jinja2")

@app.route("/success", methods = ["GET"])
def success():
    return render_template("success.jinja2", calendar = calendar)

if __name__ == "__main__":
    app.run(debug=True)