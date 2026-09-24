from flask import Flask, render_template, request, redirect,url_for,session
from werkzeug.security import generate_password_hash,check_password_hash
from database import db
from models import User, Deployment
from pair_service import PairService
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)


pair_service = PairService()

app.secret_key = "change_this_to_a_long_random_secret_key"
app.config["SECRET_KEY"] = "spacexbot-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("dashboard"))

        return "Invalid email or password"

    return render_template("login.html")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        user = User(
            username=username,
            email=email,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    deployments = Deployment.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template(
        "dashboard.html",
        deployments=deployments
    )

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/deployment", methods=["GET", "POST"])
def deployment():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        bot_name = request.form["bot_name"]
        plan = request.form["plan"]
        payment = request.form["payment"]

        deploy = Deployment(
            user_id=session["user_id"],
            bot_name=bot_name,
            plan=plan,
            payment=payment,
            status="Pending"
        )

        db.session.add(deploy)
        db.session.commit()

        return redirect(url_for("deployment"))

    deployments = Deployment.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template(
        "deployment.html",
        deployments=deployments
    )

@app.route("/payment")
def payment():
    return render_template("payment.html")

@app.route("/generate_qr", methods=["POST"])
def generate_qr():
    return "QR Code generation will be connected here."

with app.app_context():
    db.create_all()

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/pair")
def pair():
    data = pair_service.generate_qr()

    return render_template(
        "pair.html",
        qr=data["qr_image"],
        session=data["session_id"]
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(host="0.0.0.0",
 port=50800, debug=False)
