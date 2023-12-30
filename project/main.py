from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from . import db
from .models import Task

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/get_tasks_json")
def get_tasks_json():
    tasks: list[Task] = Task.query.all()
    return jsonify([task.as_dict for task in tasks])


@main.route("/profile")
@login_required
def profile():
    # user_tasks_query = db.session.execute(db.select(Task).filter_by(user_id=current_user.id)).all()
    user_tasks_query: list[Task] = (Task.query
                                    .filter_by(user_id=current_user.id)
                                    .order_by(Task.created_at.desc())
                                    .all())
    user_tasks = [task.as_dict for task in user_tasks_query]
    return render_template("profile.html", user_tasks=user_tasks)


@main.route("/add_task", methods=["POST"])
@login_required
def add_task():
    new_task_content = request.form.get("new_task_content")
    if not new_task_content:
        flash("Nelze přidat prázdný úkol.")
        return redirect(url_for("main.profile"))

    new_task = Task(content=new_task_content, created_at=datetime.now(), done=False, user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("main.profile"))
