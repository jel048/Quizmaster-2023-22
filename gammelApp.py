from flask import Flask, render_template, request, escape, url_for, flash, redirect, session
from Forms import *
from quizDB import MyDb
from quizclasses import *
from flask_login import LoginManager, current_user, login_user, logout_user
from user import User
from UserRegister import UserReg
from flask_login import login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPERSECRETS'

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        user_type = request.form['usertype']
        if user_type == "admin":
            flash('Logged in as Quiz Master')
            session['user_type'] = "admin"
            session['admin_navn'] = request.form['fornavn'] + " " + request.form['etternavn']
            return redirect(url_for('quizMaster'))
        elif user_type == "user":
            session['user_type'] = "user"
            session['kallenavn'] = request.form['kallenavn']
            with MyDb() as db:
                db.addQuizzee(session['kallenavn'])
            flash('Logged in as Quizzee')
            return redirect(url_for('quizzee'))
        
    
    return render_template('login.html', title = "LOGIN")

@app.route("/quizmaster", methods=["GET", "POST"])
def quizMaster():
    if session['user_type'] == "admin":
        return render_template("quizmaster.html", navn = session['admin_navn'])
    else:
        flash('You are not authorized to view this page')
        return redirect(url_for('quizzee'))


@app.route("/createquiz", methods=["GET", "POST"])
def createQuiz():
    if session['user_type'] == "admin":
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
def createQuestion():
    if session['user_type'] == "admin":
        form = CreateQuestionForm(request.form)
        form.Quiznavn.data = session['quiznavn']
        if request.method == "POST" and form.validate():
            question = form.question.data
            alt1 = form.alt1.data
            alt2 = form.alt2.data
            alt3 = form.alt3.data
            correct = form.correct.data
            quiznavn = form.Quiznavn.data
            with MyDb() as db:
                db.createQuestion(question, alt1, alt2, alt3, correct, quiznavn)
                flash('Spørsmål lagret')
            return render_template("createQuestion.html", form = form)
        else:
            return render_template("createQuestion.html", form = form)
    else:
        flash('You are not authorized to view this page')
        return redirect(url_for('quizzee'))


@app.route("/viewanswers", methods=["GET", "POST"] )
def viewAnswers():
    user = request.form['viewAnswers']
    with MyDb() as db:
        answ = db.showUserAnswers(user)
    answers = [UserAnswers(*answer) for answer in answ]
    return render_template("viewanswers.html", answers = answers)
    

@app.route("/viewcategories", methods=["GET"]) #Aksessert fra: quizmaster.html, quizzee.html
def viewCategories():
    with MyDb() as db:
        kategorier = [(str(item)).strip("\'(),") for item in db.showCategories()]
    return render_template("categories.html", kategorier = kategorier)

@app.route("/quizbycategory", methods=["GET", "POST"])
def quizByCategory():
    kategori = request.form['kategori']
    user = session['user_type'] #Gis til html-dok. If admin - viser quizer med link til oversikt. If user: Viser quizer med link til å svare på quiz
    with MyDb() as db:
        quizer = [(str(item)).strip("\'(),") for item in db.showQuizByCategory(kategori)]
    return render_template("quizbycategory.html", quizer = quizer, user = user)


@app.route("/redirectToAnswerQuiz", methods=["GET", "POST"])
def redirectToAnswerQuiz():
    session['quiz'] = request.form['quiz']
    return redirect(url_for('answerQuiz'))

@app.route("/redirectToquestionsbyquiz", methods=["GET", "POST"])
def redirectToQuestionsByQuiz():
    session['quiz'] = request.form['quiz']
    return redirect(url_for('questionsByQuiz'))

@app.route("/questionsbyquiz", methods=["GET", "POST"]) 
def questionsByQuiz():
    id = request.args.get('id')
    if not id:
        quiz = session['quiz']
        
        with MyDb() as db:
            result = db.questionsByQuiz(quiz)
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
                form.question.data = question.question
                form.alt1.data = question.alt1
                form.alt2.data = question.alt2
                form.alt3.data = question.alt3
                form.correct.data = question.correct
                form.Quiznavn.data = question.quiznavn
                return render_template("questionsbyquiz.html", form = form, id = id)

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
    
    return redirect(url_for('questionsByQuiz'))



@app.route("/quizzee", methods=["GET", "POST"])
def quizzee():
    return render_template("quizzee.html", kallenavn = session['kallenavn'])

@app.route("/answerquiz", methods=["GET", "POST"])
def answerQuiz():
    if 'question_index' not in session:
        session['question_index'] = 0
    if 'answers' not in session:
        session['answers'] = []
    if session['question_index'] == 0:
        quiz = session['quiz']
        with MyDb() as db:
            result = db.questionsByQuiz(quiz)
            questions = [Question(*x).__dict__ for x in result]
            session['questions'] = questions
    print(f"question index = {session['question_index']}")
    quest = session['questions']
    question = quest[session['question_index']] #Dictionary
    form = AnswerQuestionForm(request.form)
    form.alternatives.choices = [(question['alt1'],question['alt1']),(question['alt2'],question['alt2']),(question['alt3'],question['alt3'])]
    
    if request.method == "POST" and form.validate():
        user_answer = form.alternatives.data
        with MyDb() as db:
            db.userAnswer(session['kallenavn'], session['quiz'], question['question'], user_answer) #lagrer svaret i databasen
        session['answers'].append(user_answer)
        if session['question_index'] < len(session['questions']) -1: #sjekk om det er flere spm
            session['question_index'] += 1
            return redirect(url_for('answerQuiz'))
        else: #Siste spm besvart, vis resultat
            session['score'] = session['answers']
            return redirect(url_for('quizResults'))
         
    return render_template("answerquiz.html", question = question, form = form)

@app.route("/quizresults")
def quizResults():
    score = 0
    answers = session['score']
    correct_answers = [question['correct'] for question in session['questions']]
    for i in range(len(answers)):
        if answers[i] == correct_answers[i]:
            score +=1
    with MyDb() as db:
        db.userScore(session['kallenavn'], session['quiz'], score)
    session['question_index'] = 0
    session['answers'] = []
    session['questions'] = []
    session['quiz'] = None
    session['score'] = None
    return render_template("quizresults.html", score = score)

@app.route("/viewmyscores")
def viewMyScores():
    with MyDb() as db:
        result = db.viewUserScores(session['kallenavn'])
        scores = [Score(*x) for x in result]
        return render_template("viewscores.html", scores = scores, user = session['user_type'])


if __name__ == "__main__":
    app.run(debug=True)