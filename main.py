from flask import Flask, render_template, request, redirect, url_for,session
import os
from models import db,User,Task


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URL","sqlite:///task_manager_new.db")
app.secret_key = os.environ.get("FLASK_KEY")
db.init_app(app)
flask_key = os.getenv("FLASK_KEY")
print("FLASK_KEY:", flask_key)

@app.route("/",methods=["GET","POST"])
def Home():
    session["show_edit"] = False
    return render_template("index.html")

@app.route("/contact",methods=["GET","POST"])
def Contact():
    return render_template("contact.html")
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        user = User.query.filter_by(name=name).first()

        if user and user.check_password(password):
            session["name"] = user.email
            return redirect("/task")
        else:
            return render_template("login.html", error="Invalid user or password")
    return render_template("login.html")
@app.route("/signup",methods=["GET","POST"])
def signup():
  if request.method == "POST":
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    new_user = User(name=name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/login")
  return render_template("signup.html")


@app.route("/task",methods=["GET","POST"])
def task():
    if  request.method == "POST":
        return render_template("task.html", show_form=True)
    return redirect(url_for('fill'))


@app.route("/fill",methods=["GET","POST"])
def fill():
    tasks = Task.query.all()
    if request.method == "POST":
        task_date1 = request.form["taskdate"]
        task_name1 = request.form["taskname"]
        task_description1 = request.form["taskdes"]
        # task_list.append({'date': task_date1, 'name': task_name1, 'description':task_description1})
        new_task = Task(task_date=task_date1, task_name=task_name1,task_description=task_description1,email=session["name"])
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('fill'))
    return render_template("task.html",all=tasks,check_email=session["name"])

@app.route('/delete_task/<int:task_id>', methods=['GET', 'POST'])
def delete_task(task_id):
    if request.method == 'POST':
            task = Task.query.get_or_404(task_id)
            db.session.delete(task)
            db.session.commit()
            return redirect(url_for('fill'))


@app.route("/edit_task/<int:id>",methods=["GET","POST"])
def edit_task(id):
    if  request.method == "POST":
        session["target"]=id
        print(session["target"])
        session["show_edit"]=True
        return redirect(url_for('fill'))
    return redirect(url_for('fill'))


@app.route("/edit_content",methods=["GET","POST"])
def edit_content():
    t_id = session.get("target")
    target=Task.query.filter_by(id=t_id).first()
    if  request.method == "POST":
        task_date2 = request.form["edit_date"]
        task_name2 = request.form["edit_name"]
        task_description2 = request.form["edit_des"]
        target.task_date=task_date2
        target.task_name=task_name2
        target.task_description=task_description2
        db.session.commit()
        session["show_edit"] = False
        return redirect(url_for('fill'))
    return redirect(url_for('fill'))


if __name__=="__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()

    app.run(debug=False)
