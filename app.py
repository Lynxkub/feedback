from flask import Flask, render_template, redirect, session, flash 
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterUserForm, LoginUserForm, UserFeedback

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback.db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home_page():
    return redirect('/register')

@app.route('/register', methods = ['GET', 'POST'])
def register_user():

    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user =User.register(username = username, password = password, email = email, first_name = first_name, last_name = last_name)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect(f'/users/{username}')
    else: 
        return render_template('register.html', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login_user():

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f'Welcome Back, {user.username}')
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password']

    return render_template('login.html', form = form)

@app.route('/users/<username>')
def secret_page(username):
    user = User.query.get_or_404(username)
    if 'username' not in session:
        flash('Please login first!')
        return redirect('/login')
    else:
        feedback = Feedback.query.all()
        return render_template('secret.html', user = user, feedback = feedback)

@app.route('/logout')
def logout_page():
    session.pop('username')
    return redirect('/login')

@app.route('/users/<username>/feedback/add', methods = ['GET', 'POST'])
def add_feedback(username):
    user = User.query.get_or_404(username)
    if 'username' not in session:
        flash('Please login first!')
        return redirect('/login')

    form = UserFeedback()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        username = user.username
        new_feedback = Feedback(title = title, content = content, username = username)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/users/{user.username}')
    else:
        return render_template('feedback.html', form = form, user = user)

@app.route('/feedback/<int:feedback_id>/delete', methods = ['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    username = feedback.username
    if feedback.username == session['username']:
        db.session.delete(feedback)
        db.session.commit()
        flash('Feedback Deleted')
        return redirect(f'/users/{username}')
    else:
        flash('You do not have permission to do that')
        return redirect(f'/users/{username}')

@app.route('/feedback/<int:feedback_id>/update', methods = ['GET', 'POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    username = feedback.username
    logged_in_user = session['username']
    if feedback.username == session['username']:
        form = UserFeedback(obj = feedback)
    else: 
        flash('You cannot edit feedback that is not yours')
        return redirect(f'/users/{logged_in_user}')
    if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.commit()
            flash('Feedback Updated')
            return redirect (f'/users/{username}')
    else:
            return render_template('update.html', form = form, username = username)
   

@app.route('/users/<username>/delete', methods = ['POST'])
def delete_user(username):
    user = User.query.get_or_404(username)
    user_feedback = Feedback.query.filter(Feedback.username == user.username).all()
    if user.username == session['username']:
        for feedback in user_feedback:
            db.session.delete(feedback)
        db.session.delete(user)
        db.session.commit()
        flash('User and feedback posts deleted successfully')
        return redirect('/')
    else:
        flash('You need to be logged in to do that')
        return redirect('/login')
    

    


