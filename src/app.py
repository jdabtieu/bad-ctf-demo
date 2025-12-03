from flask import *
from cs50 import SQL

app = Flask(__name__)
app.config["SECRET_KEY"] = "notverysecret"

open("workshop.db", "a").close()
db = SQL("sqlite:///workshop.db")


def reset():
  # Demo: Poor password storage
  open("workshop.db", "w").close()
  db.execute("CREATE TABLE users (username text unique, password text)")
  db.execute("CREATE TABLE posts (title text, desc text)")
  db.execute("INSERT INTO posts VALUES('My First Post', 'Some text')")
  db.execute("INSERT INTO users VALUES('admin', 'mypassword')")
  return

@app.route("/")
def forum_home():
  # Demo: XSS
  posts = db.execute("SELECT * FROM posts")
  return render_template("index.html", posts=posts)

@app.route("/post", methods=["POST"])
def create_post():
  title = request.form.get("title")
  desc = request.form.get("desc")
  db.execute("INSERT INTO posts VALUES(?, ?)", title, desc)
  flash("Posted!")
  return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
  if request.method == "GET":
    return render_template("register.html")

  username = request.form.get("username")
  password = request.form.get("password")
  try:
    db.execute("INSERT INTO users VALUES(?, ?)", username, password)
    flash("User account created!")
  except Exception as e:
    flash("That username already exists")
  return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
  # Demo: SQL Injection
  if request.method == "GET":
    return render_template("login.html")

  username = request.form.get("username")
  password = request.form.get("password")
  usr = db.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
  if usr:
    flash(f"Welcome, {usr[0]['username']}")
  else:
    flash("Incorrect credentials")
  return redirect("/login")

@app.route("/adminlogin", methods=["GET", "POST"])
def admin_login():
  # Demo: Client-side validation, poor password storage
  if request.method == "GET":
    return render_template("router_login.html")
  
  ret = "Ok, since you're the admin, here are all the users:\n<pre>"
  ret += "\n".join([x["username"] + " - " + x["password"] for x in db.execute("SELECT * FROM users")])
  ret += "</pre"
  return ret

@app.route("/meta/reset")
def meta_reset():
  reset()
  flash("Done!")
  return redirect("/")
