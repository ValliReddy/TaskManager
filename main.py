from flask import Flask, render_template, request, redirect, url_for,session


app = Flask(__name__)
task_list=[]
@app.route("/",methods=["GET","POST"])
def Home():
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def login():
    return render_template("login.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
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
    app.run(debug=True)
