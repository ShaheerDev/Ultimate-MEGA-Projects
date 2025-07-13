from flask import Flask, abort, render_template, redirect, url_for, flash, request
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Skilli@123'


@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5002)