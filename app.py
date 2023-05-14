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
app.config['SECRET_KEY'] = 'SUPERSECRET'
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
            form = CreateQuestionForm()
            return render_template("createQuestion.html", form = form)
        else:
            
            return render_template("createQuestion.html", form = form)
    else:
        flash('You are not authorized to view this page')
        return redirect(url_for('quizzee'))    
    
@app.route("/createquestionessay", methods=["GET", "POST"])
@login_required
def createQuestionEssay():
    if session['isAdmin'] == True:
        form = CreateEssayQuestionForm(request.form)
        with MyDb() as db:
                id = [(str(item)).strip("\'(),") for item in db.getQuizId(session['quiznavn'])]
                quizid = int(id[0])
        if request.method == "POST" and form.validate():
            question = form.question.data
            with MyDb() as db:
                db.createQuestionEssay(quizid, question)
                flash('Spørsmål lagret')
            form = CreateEssayQuestionForm()
            return render_template("createQuestionEssay.html", form = form)
        else:
            
            return render_template("createQuestionEssay.html", form = form)
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
    if session['isAdmin'] == True:
        id = request.args.get('id')
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
                if question.alt1 != 0:
                    form = CreateQuestionForm()
                    form.id.data = question.id
                    form.idquiz.data = question.idquiz
                    form.question.data = question.question
                    form.alt1.data = question.alt1
                    form.alt2.data = question.alt2
                    form.alt3.data = question.alt3
                    selector = 1
                else:
                    form  = CreateEssayQuestionForm()
                    form.id.data = question.id
                    form.idquiz.data = question.idquiz
                    form.question.data = question.question
                    selector = 0
                return render_template("questionsbyquiz.html", form = form, id = form.id.data, selector = selector)
    else:
        flash('You are not authorized to view this page')
        return redirect(url_for('quizzee'))   

            
@app.route("/updatequestion", methods= ["GET", "POST"]) #Fortsett her. Mottar enten CreateQuestionForm eller CreateQuestionFormEssay fra questionsbyQuiz.
@login_required                                             #Må ha en if-statement.
def updateQuestion():
    if session['isAdmin'] == True:
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
    else:
        flash('You are not authorized to view this page')
        return redirect(url_for('quizzee'))
    
@app.route("/deleteconfirm", methods= ["GET", "POST"]) #confirm sletting av spm fra questionbyquiz
@login_required
def deleteConfirm():
    if session['isAdmin'] == True:
        id = request.form['delete']
        with MyDb() as db:
            q = db.getQuestion(id)
        question = Question(*q)
        return render_template("deleteconfirm.html", question = question)
    else:
        flash('You are not authorized to view this page')
        return redirect(url_for('quizzee'))

@app.route("/deleteconfirmed", methods= ["GET", "POST"])
@login_required
def deleteConfirmed():
    if session['isAdmin'] == True:
        id = request.form['deleteid']
        with MyDb() as db:
            db.deleteQuestion(id)
        flash("Spørsmål slettet.")

        return redirect(url_for('questionsByQuiz'))
    else:
        flash('You are not authorized to view this page')
        return redirect(url_for('quizzee'))

@app.route("/approveQuizes", methods= ["GET", "POST"])
@login_required
def approveQuizes():
    if session['isAdmin'] == True:
        if request.method == "POST":
            session['quizuser'] = request.form['userid']
            session['answeredquiz'] = request.form['quiz']
            return redirect(url_for('reviewQuiz'))
        else:
            with MyDb() as db:
               result = db.showUserQuizes()
            quizes = [AnsweredQuizes(*x) for x in result]
            return render_template("quizzesforapproval.html", quizes = quizes)
    else:
        flash('You are not authorized to view this page')
        return redirect(url_for('quizzee'))
    
@app.route("/kommenterquiz", methods= ["GET", "POST"])
@login_required
def kommenterQuiz():
    if session['isAdmin'] == True:
        text = request.form["kommentar"]
        idquiz = request.form["quizid"]
        userid = request.form["userid"]
        with MyDb() as db:
            kommentar = db.commentQuiz(text, idquiz, userid)
        return redirect(url_for("approveQuizes"))
    else:
        flash('You are not authorized to view this page')
        return redirect(url_for('quizzee'))

@app.route("/godkjennquiz", methods= ["GET", "POST"])
@login_required
def godkjennQuiz():
    if session['isAdmin'] == True:
        userid = request.form["userid"]
        idquiz = request.form["idquiz"]
        with MyDb() as db:
            godkjent = db.godkjennQuiz(userid, idquiz)
        return redirect(url_for("approveQuizes"))
    else:
        flash('You are not authorized to view this page')
        return redirect(url_for('quizzee'))
    
@app.route("/reviewquiz", methods= ["GET", "POST"])
@login_required
def reviewQuiz():
    if session['isAdmin'] == True:
        userid = session['quizuser']
        quizid = session['answeredquiz']
        if 'question_index' not in session:
            session['question_index'] = 0
        
        with MyDb() as db:
            result = db.questionsByQuiz(quizid)
            userAnswers = db.showUserAnswers(quizid, userid)
        questions = [Question(*x) for x in result]
        useranswers = [UserAnswers(*x)for x in userAnswers]
        question = questions[session['question_index']]
        answer = useranswers[session['question_index']]
        
        if request.method == "POST":
            if session['question_index'] < len(questions) -1: #sjekk om det er flere spm
                session['question_index'] += 1
                return redirect(url_for('reviewQuiz'))
            else:
                flash("Gjennomgang fullført")
                session['question_index'] = 0
                return redirect(url_for('approveQuizes'))
        
        
        return render_template("reviewquiz.html", question = question, answer = answer)
                
                
    else:
        flash('You are not authorized to view this page')
        return redirect(url_for('quizzee'))
    
@app.route("/kommenterspm", methods= ["GET", "POST"])
@login_required
def kommenterSpm():
    if session['isAdmin'] == True:
        text = request.form["kommentar"]
        questionid = request.form["questionid"]
        userid = request.form["userid"]
        with MyDb() as db:
            kommentar = db.commentQuestion(text, questionid, userid)
        return redirect(url_for("reviewQuiz"))
    else:
        flash('You are not authorized to view this page')
        return redirect(url_for('quizzee'))
    
@app.route("/godkjennspm", methods= ["GET", "POST"])
@login_required
def godkjennSpm():
    if session['isAdmin'] == True:
        userid = request.form["userid"]
        questionid = request.form["questionid"]
        print(userid)
        print(questionid)
        with MyDb() as db:
            godkjent = db.godkjennSpm(userid, questionid)
        return redirect(url_for("reviewQuiz"))
    else:
        flash('You are not authorized to view this page')
        return redirect(url_for('quizzee'))
    
@app.route("/deleteansweredquiz", methods= ["GET", "POST"]) #slett en hel besvart quiz
@login_required
def deleteAnsweredQuiz():
    if session['isAdmin'] == True:
        userid = request.form['userid']
        quizid = request.form['idquiz']
        with MyDb() as db:
            db.deleteQuestionsFromQuiz(userid, quizid)
        with MyDb() as db:
            db.deleteAnsweredQuiz(userid, quizid)
        return redirect(url_for('approveQuizes'))
    else:
        flash('You are not authorized to view this page')
        return redirect(url_for('quizzee'))
    
@app.route("/deleteansweredquestion", methods= ["GET", "POST"]) #slett ett besvart spørsmål inni en quiz
@login_required
def deleteAnsweredQuestion():
    if session['isAdmin'] == True:
        userid = request.form['userid']
        questionid = request.form['questionid']
        with MyDb() as db:
            db.deleteAnsweredQuestion(userid, questionid)
        flash("Spørsmål slettet")
        return redirect(url_for('approveQuizes'))
    else:
        flash('You are not authorized to view this page')
        return redirect(url_for('quizzee'))

#answerquiz essay textbox må gjøres større.
#omgjør alle alt1 = 0 til alt1 = None
#finn ut hvordan jeg skal gjøre det med å implementere forskjellige typer spm
#fiks alle templates
#Gjør litt mer ut av designet
#publisering på kark
#rapport, video, kildekode, ERdiagram


    
@app.route("/quizzee", methods=["GET", "POST"])
@login_required
def quizzee():
    return render_template("quizzee.html")

@app.route("/answerquiz", methods=["GET", "POST"])
@login_required
def answerQuiz():
    if 'question_index' not in session:
        session['question_index'] = 0
    if session['question_index'] == 0:
        
        with MyDb() as db:
            id = [(str(item)).strip("\'(),") for item in db.getQuizId(session['quiz'])]
            session["quizid"] = int(id[0])
            result = db.questionsByQuiz(session["quizid"])
        questions = [Question(*x).__dict__ for x in result]
        session['questions'] = questions
    print(f"question index = {session['question_index']}")
    quest = session['questions']
    question = quest[session['question_index']]
    print(question['alt1'])
    if question['alt1'] != None: #Testing for essayQuestions
        form = AnswerQuestionForm(request.form)
        form.answer.choices = [(question['alt1'],question['alt1']),(question['alt2'],question['alt2']),(question['alt3'],question['alt3'])]
    else:
        form = AnswerQuestionFormEssay(request.form)
        
    
    if request.method == "POST" and form.validate():
        user_answer = form.answer.data 
        with MyDb() as db:
            db.userAnswer(session["userID"], question['id'], user_answer) #lagrer svaret i databasen
        if session['question_index'] < len(session['questions']) -1: #sjekk om det er flere spm
            session['question_index'] += 1
            return redirect(url_for('answerQuiz'))
        else: #Siste spm besvart, vis resultat
            with MyDb() as db:
                complete = db.quizcomplete(session["userID"], session["quizid"])
            return redirect(url_for('completed'))
         
    return render_template("answerquiz.html", question = question, form = form)

@app.route("/completed")
@login_required
def completed():
    session['question_index'] = 0
    session['answers'] = []
    session['questions'] = []
    session['quiz'] = None
    session["quizid"] = None
    return render_template("completed.html")

@app.route("/myresults") #If quiz godkjent av admin - vises på denne siden. Kan så klikke inn på quiz for å se godkjente spm, og kommentarer.
@login_required
def myResults():
    with MyDb() as db:
        results = db.getQuizesMyResults(session["userID"])
    approvedquizes = [ApprovedQuizes(*x) for x in results]
    return render_template("myresults.html", approvedquizes = approvedquizes)


@app.route("/myquizresults", methods=["GET", "POST"]) #needs work
@login_required
def myQuizResults():
    quizid = request.form['quiz']
    with MyDb() as db:
        results = db.getQuestionsMyResults(session["userID"], quizid)
    approvedquestions = [ApprovedQuestions(*x) for x in results]
    return render_template("myquestionresults.html", approvedquestions = approvedquestions)



if __name__ == "__main__":
    app.run(debug=True)
