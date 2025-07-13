from flask import Flask, abort, render_template, redirect, url_for, flash, request
import smtplib
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Your Secret Key'


@app.route("/")
def home(): 
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/github")
def github():
    return render_template("github.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        my_email = "Your Email"
        password = "Your Password"

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="Addres You Wan to send to",
                msg=f"Subject: New Message from Blog Website \n\n {name} \n {email} \n {phone} \n {message}")

        return render_template("contact.html", message_sent=True)
    return render_template("contact.html", message_sent=False)

@app.route("/projects")
def projects():
    return render_template("projects.html")

if __name__ == "__main__":
    app.run(debug=True, port=5002)
