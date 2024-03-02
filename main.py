from flask import Flask, render_template, request, redirect, url_for,session
from models import db,Task,User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_manager_new.db'
app.secret_key = "secret_keying"
db.init_app(app)

task_list=[]
@app.route("/",methods=["GET","POST"])
def Home():
    return render_template("index.html")

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
    return render_template("task.html")

@app.route("/fill",methods=["POST"])
def fill():
    task_date = request.form["taskdate"]
    task_name = request.form["taskname"]
    task_description = request.form["taskdes"]
    task_list.append({'date': task_date, 'name': task_name, 'description':task_description})
    return render_template("task.html",all=task_list)






if __name__=="__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()

    app.run(debug=True)
