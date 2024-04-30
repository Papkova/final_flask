import os
from flask import Flask, render_template, request, redirect, abort
from flask_login import LoginManager
from .models import Post, session, User
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/flask_post")
def flask_post():
    return render_template("flask_post.html")


@app.route("/create_post", methods=["POST", "GET"])
def create_post():
    if request.method == "POST":
        title = request.form["title"]
        intro = request.form["intro"]
        text = request.form["text"]

        post = Post(
            title=title,
            intro=intro,
            text=text
        )
        try:
            session.add(post)
            session.commit()
            return redirect("/posts")
        except Exception as exc:
            return f"Пpи збереженні запису у базу даних виникла помилка: {exc}"
    else:
        return render_template("create_post.html")


@app.route("/posts")
def list_post():
    posts = session.query(Post).order_by(Post.date.desc()).all()
    return render_template("posts.html", posts=posts)


@app.route("/posts/<int:id>/")
def post_detail(id):
    post = session.query(Post).get(id)
    return render_template("post_detail.html", post=post)


@app.route("/posts/<int:id>/delete")
def post_delete(id):
    post = session.query(Post).get(id)
    if post is None:
        abort(404)

    try:
        session.delete(post)
        session.commit()
        return redirect("/posts")
    except Exception as exc:
        return f"При видаленні виникла помилка: {exc}"


@app.route("/posts/<int:id>/update", methods=["POST", "GET"])
def post_update(id):
    post = session.query(Post).get(id)

    if request.method == "POST":
        post.title = request.form["title"]
        post.intro = request.form["intro"]
        post.text = request.form["text"]

        try:
            session.commit()
            return redirect("/posts")
        except Exception as exc:
            return f"При оновленні запису виникла помилка: {exc}"
    else:
        return render_template("post_updata.html", post=post)