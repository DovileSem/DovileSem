from flask import Flask, render_template, url_for, request, redirect, request, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from flask_login import UserMixin, logout_user, login_required, LoginManager,current_user

from flask import Flask, render_template, flash, request, redirect, url_for
from forms import LoginForm, RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Nurodome pagrindinio failo pavadinima
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)

app.config['SECRET_KEY'] = os.urandom(32)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'Login'

class Article(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return '<Article %r>' % self.id

class User_data(db.Model,UserMixin):
    __tablename__ = 'Vartotojas'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable=False,unique=True)
    password = db.Column(db.String, nullable = False)

    
    def __init__(self, username, password):
        self.username = username
        self.password = password

    
@login_manager.user_loader
def load_user(user_id):
    return User_data.query.get(int(user_id))        

with app.app_context():
    db.create_all()




@app.route('/')
@app.route('/home')
# @login_required
def index(): 
    # name = current_user.username 
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template("about.html")

# Prisiregistruoti
@app.route('/register' , methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method = 'sha256')             #uzhashintas slaptazodis
        username = form.username.data
        password = hashed_password


        new_register =User_data(username=username, password=password)

        db.session.add(new_register)

        db.session.commit()

        return redirect(url_for('Login'))


    return render_template('register.html', form=form)


# Prisijungti
@app.route('/login' , methods = ['GET', 'POST'])
def Login():
    form = LoginForm()

    if form.validate_on_submit():
        if request.form['username'] != request.form.get('username') or request.form['password'] != request.form.get('password'):
            flash("Blogai ivedėte prisijungimo duomenis, bandykite dar kart")

        else:
            return redirect(url_for('base_log')) 



    return render_template('login.html', form = form)


@app.route('/base_log')
def base_log():
    return render_template("baselog.html")

# Atsijungti
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('base'))


@app.route('/base')
def base():
    return render_template("base.html")


# Straipsniai

@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/posts/<int:id>/del')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
         db.session.delete(article)
         db.session.commit()
         return redirect('/posts')
    except:
        return "Trinant įrašą įvyko klaida"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "Redaguojat tekstą įvyko klaida."
    else:
        
        return render_template("post_update.html", article=article)


@app.route('/contact_log')
def contact_log():
    return render_template("contact_log.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/price')
def price():
    return render_template("price.html")

@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Įvedant tekstą įvyko klaida"
    else:
        return render_template("create-article.html")

@app.route("/contac_log", methods=["POST"])
def foo():

  mail = MIMEMultipart("alternative")
  mail["Subject"] = "Bla bla bla"
  mail["From"] = "d.semaskiene@gmail.com"
  mail["To"] = "d.semaskiene@gmail.com"

 
  data = dict(request.form)
  msg = "<html><head></head><body>"
  for key, value in data.items():
    msg += key + " : " + value + "<br>"
  msg += "</body></html>"
  mail.attach(MIMEText(msg, "html"))

 
  mailer = smtplib.SMTP("smtp.gmail.com")
  mailer.sendmail('xxxx@gmail.com', 'xxxxxxxxxxxx@gmail.com', mail.as_string())
  mailer.quit()

  res = make_response("OK", 200)
  return res
if __name__ == "__main__":
    app.run(debug=True)
