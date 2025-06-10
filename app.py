from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect
import json
import uuid
"""Simple Blog Web-App"""
app = Flask(__name__)


def fetch_post_by_id(post_id):
    """getter for the post"""
    with open("data.json", "r") as grap_it:
        posts = json.load(grap_it)
        for post in posts:
            if post["id"] == post_id:
                return post
        return None


@app.route('/')
def index():
    """GET funktion main page"""
    with open("data.json", "r") as grap_it:
        blog = json.load(grap_it)
    return render_template("index.html", posts=blog, title_blog="Was so passiert im Hause Pape-Ludwig")


@app.route("/add", methods=["GET", "POST"])
def add():
    """create a new post reading and writing JSON Data"""
    if request.method == "POST":
        new_post = {}
        new_post["id"] = str(uuid.uuid4())
        new_post["title"] = request.form.get("title")
        new_post["author"] = request.form.get("author")
        new_post["content"] = request.form.get("content")
        with open("data.json", "r") as grap_it:
            d = json.load(grap_it)
            d.append(new_post)
        with open("data.json", "w") as dump_it:
            json.dump(d, dump_it)
        return redirect(url_for("index"))
    return render_template("add.html")


@app.route("/delete/<post_id>")
def delete(post_id):
    """delete a post to and out of JSON"""
    with open("data.json", "r") as grap_it:
        posts = json.load(grap_it)
        post = fetch_post_by_id(post_id)
        if post is None:
            return "Post not found", 404
        posts.remove(post)
        with open("data.json", "w") as dump_it:
            json.dump(posts, dump_it)
        return redirect(url_for("index"))


@app.route("/update/<post_id>", methods=["GET", "POST"])
def update(post_id):
    """Update a poste in and out a JSON Data"""
    with open("data.json", "r") as grap_it:
        posts = json.load(grap_it)
        post = fetch_post_by_id(post_id)
        index = posts.index(post)
    if post is None:
        return "Post not found", 404
    if request.method == "POST":
        posts[index]["title"] = request.form.get("title")
        posts[index]["author"] = request.form.get("author")
        posts[index]["content"] = request.form.get("content")
        with open("data.json", "w") as dump_it:
            json.dump(posts, dump_it)
            return redirect(url_for("index"))
    else:
        return render_template("update.html", post=post)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
