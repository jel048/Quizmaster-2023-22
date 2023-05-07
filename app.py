from flask import Flask, render_template, request, url_for, flash, redirect, session
from markupsafe import escape
from Forms import *
from quizDB import MyDb
from quizclasses import *
from UserRegister import UserReg
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from user import User
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPERSECRETs'
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    with UserReg() as db:
        user = User(*db.getUserById(user_id))
    return user

@app.route('/')
@app.route('/index')
def index():
    return render_template("login.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        with UserReg() as db:
            usr = db.getUser(username)
            if usr:
                user = User(*usr)
                if user.check_password(password):
                    login_user(user, remember=True)
                if user.isAdmin == 1:
                    session['isAdmin'] = True
                else:
                    session['isAdmin'] = False
                session["userID"] = user.id
            return redirect(url_for('index'))
        
@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/quizmaster", methods=["GET", "POST"])
@login_required
def quizMaster():
    if session['isAdmin'] == True:
        return render_template("quizmaster.html")
    else:
        flash('You are not authorized to view this page')
        return redirect(url_for('quizzee'))
    
    
@app.route("/createquiz", methods=["GET", "POST"])
@login_required
def createQuiz():
    if session['isAdmin'] == True:
        form = quizForm(request.form)
        if request.method == "POST" and form.validate():
            quiznavn = form.quiznavn.data
            kategori = form.kategori.data
            with MyDb() as db:
                db.createQuiz(quiznavn, kategori)
                flash(f'Success, {quiznavn} created!')
                session['quiznavn'] = quiznavn

            return redirect(url_for('createQuestion'))
        else:
            return render_template("createQuiz.html", form = form)
    else:
        flash('You are not authorized to view this page')
        return redirect(url_for('quizzee'))
    
@app.route("/createQuestion", methods=["GET", "POST"])
@login_required
def createQuestion():
    if session['isAdmin'] == True:
        form = CreateQuestionForm(request.form)
        with MyDb() as db:
                id = [(str(item)).strip("\'(),") for item in db.getQuizId(session['quiznavn'])]
                quizid = int(id[0])
        if request.method == "POST" and form.validate():
            question = form.question.data
            alt1 = form.alt1.data
            alt2 = form.alt2.data
            alt3 = form.alt3.data
            with MyDb() as db:
                db.createQuestion(quizid, question, alt1, alt2, alt3)
                flash('Spørsmål lagret')
            return render_template("createQuestion.html", form = form)
        else:
            return render_template("createQuestion.html", form = form)
    else:
        flash('You are not authorized to view this page')
        return redirect(url_for('quizzee'))    
    
    
@app.route("/viewcategories", methods=["GET"]) #Aksessert fra: quizmaster.html, quizzee.html
@login_required
def viewCategories():
    with MyDb() as db:
        kategorier = [(str(item)).strip("\'(),") for item in db.showCategories()]
    return render_template("categories.html", kategorier = kategorier)

@app.route("/quizbycategory", methods=["GET", "POST"])
@login_required
def quizByCategory():
    kategori = request.form['kategori']
    with MyDb() as db:
        quizer = [(str(item)).strip("\'(),") for item in db.showQuizByCategory(kategori)]
    return render_template("quizbycategory.html", quizer = quizer)

@app.route("/redirectToAnswerQuiz", methods=["GET", "POST"])
def redirectToAnswerQuiz():
    session['quiz'] = request.form['quiz']
    return redirect(url_for('answerQuiz'))

@app.route("/redirectToquestionsbyquiz", methods=["GET", "POST"])
def redirectToQuestionsByQuiz():
    session['quiz'] = request.form['quiz']
    return redirect(url_for('questionsByQuiz'))

@app.route("/questionsbyquiz", methods=["GET", "POST"]) 
@login_required
def questionsByQuiz():
    id = request.args.get('id')
    print(id)
    if not id:
        quiz = session['quiz']
        with MyDb() as db:
            id = [(str(item)).strip("\'(),") for item in db.getQuizId(quiz)]
            quizid = int(id[0])
        
        with MyDb() as db:
            result = db.questionsByQuiz(quizid)
            questions = [Question(*x) for x in result]
        if len(questions)< 1: #Redirect om quizen er tom, for å forhindre error
            return redirect(url_for('quizMaster'))
        
        return render_template("questionsbyquiz.html", questions = questions)
    else:
        with MyDb() as db:
            spm = db.getQuestion(id)
        if spm is None:
            return render_template('error.html',
                                   msg='Invalid parameter')
        else:
            question = Question(*spm)
            form = CreateQuestionForm()
            form.id.data = question.id
            form.idquiz.data = question.idquiz
            form.question.data = question.question
            form.alt1.data = question.alt1
            form.alt2.data = question.alt2
            form.alt3.data = question.alt3
            return render_template("questionsbyquiz.html", form = form, id = form.id.data)
            
            
@app.route("/updatequestion", methods= ["GET", "POST"])
def updateQuestion():
    form = CreateQuestionForm(request.form)
    id = form.id.data
    if request.method == "POST" and form.validate():
        id = form.id.data
        question = form.question.data
        alt1 = form.alt1.data
        alt2 = form.alt2.data
        alt3 = form.alt3.data
        quest = (question, alt1, alt2, alt3, id)
        
        with MyDb() as db:
            update = db.updateQuestion(quest)
        
        return redirect(url_for("questionsByQuiz"))
    else:
        return render_template("questionsbyquiz.html", form = form, id = id)
    
@app.route("/deleteconfirm", methods= ["GET", "POST"]) #confirm sletting av spm fra questionbyquiz
def deleteConfirm():
    id = request.form['delete']
    with MyDb() as db:
        q = db.getQuestion(id)
    question = Question(*q)
    return render_template("deleteconfirm.html", question = question)

@app.route("/deleteconfirmed", methods= ["GET", "POST"])
def deleteConfirmed():
    id = request.form['deleteid']
    with MyDb() as db:
        db.deleteQuestion(id)
    flash("Spørsmål slettet.")
    
    return redirect(url_for('questionsByQuiz'))



#answerquiz for user
#admin gå igjennom besvarte quizer - kommentere og godkjenne
#menyvalg for user å se ferdig godkjente/kommenterte quizer
#admin mulighet til å slette enkeltspm og hel quiz
#finn ut hvordan jeg skal gjøre det med å implementere forskjellige typer spm
#fiks alle templates
#Gjør litt mer ut av designet
#Løsningen må ha beskyttelse mot XSS, CSRF og SQL injection
#publisering på kark
#rapport, video, kildekode, ERdiagram

    
    
    
@app.route("/quizzee", methods=["GET", "POST"])
@login_required
def quizzee():
    return render_template("quizzee.html")

@app.route("/answerquiz", methods=["GET", "POST"])
def answerQuiz():
    if 'question_index' not in session:
        session['question_index'] = 0
    if session['question_index'] == 0:
        quiz = session['quiz'] #PROBLEMET ER HER - SESSION QUIZ INNEHOLDER QUIZNAVN, IKKE QUIZID. FIX.
        with MyDb() as db:
            result = db.questionsByQuiz(quiz)
            questions = [Question(*x).__dict__ for x in result]
            session['questions'] = questions
            print(session['questions'])
    print(f"question index = {session['question_index']}")
    quest = session['questions']
    question = quest[session['question_index']] #Dictionary  PROBLEMER HER- INDEX OUT OF RANGE?
    form = AnswerQuestionForm(request.form)
    form.alternatives.choices = [(question['alt1'],question['alt1']),(question['alt2'],question['alt2']),(question['alt3'],question['alt3'])]
    
    if request.method == "POST" and form.validate():
        user_answer = form.alternatives.data
        with MyDb() as db:
            db.userAnswer(session["userID"], question['id'], user_answer) #lagrer svaret i databasen
        if session['question_index'] < len(session['questions']) -1: #sjekk om det er flere spm
            session['question_index'] += 1
            return redirect(url_for('answerQuiz'))
        else: #Siste spm besvart, vis resultat
            return redirect(url_for('completed'))
         
    return render_template("answerquiz.html", question = question, form = form)

@app.route("/quizresults")
def completed():
    session['question_index'] = 0
    session['answers'] = []
    session['questions'] = []
    session['quiz'] = None
    return render_template("completed.html")

@app.route("/myresults") #If quiz godkjent av admin - vises på denne siden. Kan så klikke inn på quiz for å se godkjente spm, og kommentarer.
def myResults():
        return render_template("viewscores.html")


if __name__ == "__main__":
    app.run(debug=True)
