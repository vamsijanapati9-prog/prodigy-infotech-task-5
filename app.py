
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from flask import Blueprint

app = Flask(__name__)
app.secret_key = "secretkey"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

posts = []

# Create blueprint for marketing
marketing_bp = Blueprint('marketing', __name__, template_folder='templates')

@marketing_bp.route('/marketing')
def marketing():
    return render_template('marketing.html')

# Register blueprint
app.register_blueprint(marketing_bp)

@app.route("/")
def home():
    return render_template("feed.html", posts=posts)

@app.route("/create", methods=["POST"])
def create_post():
    content = request.form.get("content")
    file = request.files.get("media")

    filename = None
    if file and file.filename != "":
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    posts.insert(0, {"content": content, "media": filename, "likes": 0})
    return redirect(url_for("home"))

@app.route("/like/<int:post_id>")
def like(post_id):
    posts[post_id]["likes"] += 1
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
