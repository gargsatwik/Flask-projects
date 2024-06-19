import smtplib
import wtforms
from flask import Flask, render_template, request, url_for, redirect
import datetime
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
# from openai import OpenAI
import requests
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config["STATIC_FOLDER"] = "static"
year = datetime.datetime.now().year
Bootstrap5(app)
MY_EMAIL = os.environ.get('MY_EMAIL')
PASSWORD = os.environ.get('PASSWORD')


class ContactForm(FlaskForm):
    name = wtforms.StringField('Name', validators=[wtforms.validators.DataRequired()])
    email = wtforms.EmailField('Email', validators=[wtforms.validators.DataRequired()])
    phone_no = wtforms.IntegerField('Phone number', validators=[wtforms.validators.DataRequired()])
    message = wtforms.StringField('Message', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Submit')


@app.route('/')
def home():
    return render_template('index.html', year=year)


@app.route('/about')
def about():
    return render_template('about.html', year=year)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'GET':
        return render_template('contact.html', year=year, form=form)
    elif request.method == 'POST':
        if form.validate_on_submit:
            name = form.name.data
            email = form.email.data
            phone_no = form.phone_no.data
            message = form.message.data
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=PASSWORD)
                connection.sendmail(from_addr=MY_EMAIL,
                                    to_addrs=os.environ.get('TO_ADDRESS'),
                                    msg=f"Subject:Contact Request\n\nName: {name}\nEmail: {email}\n"
                                        f"Phone number: {phone_no}\nMessage: {message}")
        return redirect(url_for('contact'))


@app.route('/projects')
def projects():
    projects_headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    repositories = requests.get(url=f"https://api.github.com/user/repos", headers=projects_headers).json()
    # for project in repositories:
    #     data = client.images.generate(
    #         model="dall-e-3",
    #         prompt=project['name'],
    #         n=1,
    #         size="1024x1024",
    #         quality="standard"
    #     )
    #     img_url = data.data[0].url
    #     project['img_url'] = img_url
    return render_template('projects.html', year=year, projects=repositories,)


@app.route('/experiences')
def experiences():
    return render_template('experiences.html', year=year)


if __name__ == '__main__':
    app.run(debug=True)
