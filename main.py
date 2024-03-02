from flask import Flask, render_template, request, redirect, url_for,session


app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def Home():
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def login():
    return render_template("login.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
    return render_template("signup.html")

if __name__=="__main__":
    app.run(debug=True)
