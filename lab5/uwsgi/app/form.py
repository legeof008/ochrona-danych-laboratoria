from flask import Flask
from flask import request, redirect
from flask import make_response, render_template
from uuid  import uuid4
from bcrypt import checkpw

# global objects
app = Flask(__name__)
hashed_password = b'$2b$12$YegDi5sS7DB4QCA9/XfEGu4P7VFgKs5qaXjUqW87QI9V2kv3qFJaC'
authenticated_users = {"71991798-5b27-4e88-85a4-1beec1e6da58" : "bach"}

@app.route("/", methods=["GET"])
def index():
  sid = request.cookies.get("sid")
  if sid in authenticated_users:
    return render_template("homepage.html")
  return redirect("/authenticate", code=302)

@app.route("/authenticate", methods=["GET", "POST"])
def authenticate():
  if request.method == "GET":
    return render_template("login-form.html")

  username = request.form.get("username", "")
  password = request.form.get("password", "")

  if username == "admin" and checkpw(bytes(password, "utf-8"), hashed_password):
    sid = str(uuid4())

    authenticated_users[sid] = "admin"
    response = redirect("/", code=302)
    response.set_cookie("sid", sid)
    return response

  return "Wrong username or password", 400
