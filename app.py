from flask import Flask, render_template, redirect, session, request
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///authenticationflask"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    return redirect("/register")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
        db.session.add(user)
        db.session.commit()

        session['username'] = user.username
        
        return redirect(f"/users/{user.username}")

    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(f"/users/{session['username']}")
    
    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password."]
    return render_template("login.html", form=form)
        

@app.route("/logout")
def logout():
    """logout route"""

    session.pop("username")
    return redirect("/login")


@app.route('/users/<username>')
def show_user(username):

    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    user = User.query.get(username)
    form = DeleteForm()

    return render_template("show.html", user=user, form=form)

@app.route('/users/<username>/delete', methods=['POST'])
def remove_user(username):
    """Remove user"""

    if "username" not in session or username != session["username"]:
        raise Unauthorized()
    
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")

@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
def new_feedback(username):
    """Show feedback form"""

    if "username" not in session or username != session["username"]:
        raise Unauthorized()
    
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(title=title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    
    else:
        return render_template("new.html", form=form)
    

@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def update_fb(feedback_id):
    """update feedback form"""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
    
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    
    return render_template("/edit.html", form=form, feedback=feedback)

@app.route('/feedback/<int:feedback_id>/delete', methods=["POST"])
def delete_fb(feedback_id):

    feedback = Feedback.query.get(feedback_id)
    if 'username' not in session or feedback.username != session['username']:
        raise Unauthorized()
    
    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")

# /feedback/<int:feedback_id>/update get post
# /feedback/<int:feedback_id>/delete post
