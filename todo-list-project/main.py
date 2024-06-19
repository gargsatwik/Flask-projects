from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import datetime
from flask_bootstrap import Bootstrap

app = Flask(__name__)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tasks.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)
Bootstrap(app)
year = datetime.datetime.now().year


class Task(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    starred: Mapped[bool] = mapped_column(Boolean, default=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template("index.html", all_tasks=sorting_tasks(tasks), year=year)


@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    new_task_description = request.form['task']
    new_task = Task(task=new_task_description)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/star/<task_id>', methods=['GET', 'POST'])
def is_starred(task_id):
    task = Task.query.get(task_id)
    if task.starred:
        task.starred = False
    elif not task.starred:
        task.starred = True
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/delete/<task_id>', methods=['GET', 'POST'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/complete/<task_id>', methods=['POST'])
def complete(task_id):
    task = Task.query.get(task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('home'))


def sorting_tasks(tasks):
    starred_tasks = []
    normal_tasks = []
    completed_tasks = []
    for task in tasks:
        if task.completed:
            task.starred = False
            completed_tasks.append(task)
        elif task.starred:
            starred_tasks.append(task)
        else:
            normal_tasks.append(task)
    all_tasks = starred_tasks + normal_tasks + completed_tasks
    return all_tasks


if __name__ == "__main__":
    app.run(debug=True)

#frontend improvement
