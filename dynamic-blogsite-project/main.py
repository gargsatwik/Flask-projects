from flask import Flask, render_template, url_for, request
import datetime
import requests
import smtplib
import os

app = Flask(__name__)
my_email = os.environ.get('MY_EMAIL')
password = os.environ.get('PASSWORD')


@app.route('/')
def home():
    response = requests.get(url="https://api.npoint.io/83e600f3b8ed04b0c1b6").json()
    return render_template("index.html", link=url_for("static", filename="css/styles.css"),
                           year=datetime.datetime.now().year, heading="Satwik's Blog", tagline="A project",
                           content=response)


@app.route('/about')
def about():
    return render_template("about.html", heading="About Me", tagline="This is what i do",
                           image_link=url_for("static", filename="static/assets/img/about-bg.jpg"))


@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == "GET":
        return render_template("contact.html", heading="Contact Me",
                               tagline="Have questions? I have answers",
                               image_link=url_for("static", filename="static/assets/img/contact-bg.jpg"))
    elif request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone']
        message = request.form['message']
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email,
                                to_addrs=os.environ.get('TO_ADDRESS'),
                                msg=f"Subject:New User/n/nName: {name}/nEmail: {email}/nPhone Number: {phone_number}/n"
                                    f"Message: {message}")
        return render_template("contact.html", heading="Successfully sent message",
                               tagline="Have questions? I have answers",
                               image_link=url_for("static", filename="static/assets/img/contact-bg.jpg"))


@app.route('/post/<num>')
def post(num):
    response = requests.get(url="https://api.npoint.io/83e600f3b8ed04b0c1b6").json()
    content = None
    heading = None
    for blog in response:
        if blog['id'] == int(num):
            content = blog
            heading = content['title']
    return render_template("post.html", content=content, num=num, year=datetime.datetime.now().year,
                           link=url_for("static", filename="css/styles.css"), heading=heading)


if __name__ == "__main__":
    app.run(debug=True)
