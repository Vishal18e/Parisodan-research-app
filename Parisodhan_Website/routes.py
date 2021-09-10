from flask import redirect,url_for,render_template,request,session,flash
import os
from Parisodhan_Website import app, db, bcrypt
from Parisodhan_Website.paragraph import paragraph_answer_question
from Parisodhan_Website.pdf_wiki_search import DocumentReader
from Parisodhan_Website.forms import Registration, Login
from Parisodhan_Website.models import User
from flask_login import login_user, current_user, logout_user, login_required

import wikipedia as wiki

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

user=User.query.filter_by(username='Admin').first()
if not user:
    user=User(username='Admin', email='admin@parisodhan.com', 
        password=bcrypt.generate_password_hash('08c00bb739a02160b3d097f8377ba739').decode('utf-8'))
    db.session.add(user)
    db.session.commit()

@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html", container='wrapper', homeactive='active')

@app.route("/about")
def about():
    return render_template("about.html", title='About', container='wrapper', aboutactive='active')

@app.route("/team")
def team():
    return render_template("team.html", title='Our Team', container='wrapper', teamactive='active')

@app.route('/paragraph', methods=['GET', 'POST'])
@login_required
def paragraph():
  
    if request.method == 'POST':
        form = request.form
        result = []
        bert_abstract = form['paragraph']
        question = form['question']
        result.append(form['question'])
        result.append(paragraph_answer_question(question, bert_abstract))
        result.append(form['paragraph'])

        return render_template("paragraph.html",result = result, title='Paragraph Search', container='wrapper2', resourceactive='active')

    return render_template("paragraph.html", title='Paragraph Search', container='wrapper2', resourceactive='active')

reader = DocumentReader("deepset/bert-base-cased-squad2") 

@app.route('/uploader', methods=['GET','POST'])
@app.route('/pdfsearch', methods=['GET', 'POST'])
@login_required
def pdfsearch():
  
    if request.method == 'POST':
        f = request.files['file']
        f.filename = "sample.pdf"
        f.save(os.path.join(app.root_path,'UPLOAD_FOLDER', f.filename))
        form = request.form
        result = []
        question = form['question']
        text = ""
        for page_layout in extract_pages("Parisodhan_Website/UPLOAD_FOLDER/sample.pdf"):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    text+=element.get_text()
        reader.tokenize(question,text)
        result.append(question)
        result.append(reader.get_answer())
        return render_template("pdfsearch.html",result = result, title='PDF Search', container='wrapper2', resourceactive='active')

    return render_template("pdfsearch.html", title='PDF Search', container='wrapper2', resourceactive='active')


@app.route('/wikisearch', methods=['GET', 'POST'])
@login_required
def wikisearch():
  
    if request.method == 'POST':
        form = request.form
        result = []
        # bert_abstract = form['paragraph']
        question = form['question']
        results = wiki.search(question)
        page = wiki.page(results[0])
        bert_abstract = page.content
        result.append(form['question'])
        reader.tokenize(question,bert_abstract)
        result.append(reader.get_answer())
        #   result.append(bert_abstract)

        return render_template("wikisearch.html",result = result, title='Wiki Search', container='wrapper2', resourceactive='active')

    return render_template("wikisearch.html", title='Wiki Search', container='wrapper2', resourceactive='active')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=Registration()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered! Lets login to continue!', category='success')
        return redirect(url_for('login'))
    return render_template('registration.html', title='registration', container='wrapper', registrationactive='active', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=Login()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get("next")
            if next_page :
                return redirect(next_page)
            else:
                if user.username=='Admin':
                    flash('Welcome Admin!', category='success')
                else:
                    flash('You have successfully logged in!', category='success')
                return redirect(url_for('index'))
        else :
            flash('Try Again!', category='danger')
    return render_template('login.html', title='login', container='wrapper', loginactive='active', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))