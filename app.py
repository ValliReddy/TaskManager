from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)
app.secret_key = os.getenv("SECRET_KEY")
@app.route("/", methods=["GET", "POST"])
def Home():
    session["show_edit"] = False
    return render_template("index.html")

@app.route("/contact", methods=["GET", "POST"])
def Contact():
    return render_template("contact.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        user = mongo.db.users.find_one({"name": name})

        if user and bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
            session["name"] = user["email"]
            return redirect("/task")
        else:
            return render_template("login.html", error="Invalid user or password")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        new_user = {"name": name, "email": email, "password": hashed_password}
        mongo.db.users.insert_one(new_user)
        return redirect("/login")
    return render_template("signup.html")

@app.route("/task", methods=["GET", "POST"])
def task():
    if request.method == "POST":
        return render_template("task.html", show_form=True)
    return redirect(url_for('fill'))

@app.route("/fill", methods=["GET", "POST"])
def fill():
    tasks = list(mongo.db.tasks.find({"email": session.get("name")}))
    show_edit = session.get("show_edit", False)
    target = session.get("target", None)
    if request.method == "POST":
        task_date1 = request.form["taskdate"]
        task_name1 = request.form["taskname"]
        task_description1 = request.form["taskdes"]
        new_task = {
            "task_date": task_date1,
            "task_name": task_name1,
            "task_description": task_description1,
            "email": session["name"]
        }
        mongo.db.tasks.insert_one(new_task)
        session["show_edit"] = False
        return redirect(url_for('fill'))
    return render_template("task.html", all=tasks, check_email=session.get("name"), show_edit=show_edit, target=target)


@app.route('/delete_task/<task_id>', methods=['GET', 'POST'])
def delete_task(task_id):
    if request.method == 'POST':
        mongo.db.tasks.delete_one({"_id": ObjectId(task_id)})
        return redirect(url_for('fill'))


@app.route("/edit_task/<task_id>", methods=["POST"])
def edit_task(task_id):
    session["target"] = task_id
    session["show_edit"] = True
    return redirect(url_for('fill'))


@app.route("/edit_content", methods=["POST"])
def edit_content():
    t_id = session.get("target")
    task_date2 = request.form["edit_date"]
    task_name2 = request.form["edit_name"]
    task_description2 = request.form["edit_des"]
    mongo.db.tasks.update_one({"_id": ObjectId(t_id)}, {
        "$set": {
            "task_date": task_date2,
            "task_name": task_name2,
            "task_description": task_description2
        }
    })
    session["show_edit"] = False
    session["target"] = None
    return redirect(url_for('fill'))


# if __name__ == "__main__":
#     app.run(debug=True)