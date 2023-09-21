from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Survey, Question, satisfaction_survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config["SECRET_KEY"] ="secret" 

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



@app.route("/")
def main_page():
    survey = satisfaction_survey
    return render_template("main_page.html", survey=survey, button="START")

@app.route("/start/")
def start():
    
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def handle_answer():
    choice = request.form["answer"]

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    return redirect(f"/questions/{len(responses)}/")


@app.route("/questions/<int:ques_num>/")
def question_page(ques_num):
    survey_length = len(satisfaction_survey.questions)
    responses = session.get(RESPONSES_KEY)
 
    
    if ques_num < survey_length:
        question = satisfaction_survey.questions[ques_num]
     
        next= f"/questions/{int(ques_num) + 1}"
    
    elif (len(responses) != ques_num):
    
        flash(f"Wrong question id: {ques_num}")
        return redirect(f"/questions/{len(responses)}")
    else:
        question = ""

        return redirect("/thanks/")

    return render_template("question.html", question=question, button="NEXT", next=next)

@app.route("/thanks/")
def thanks_page():
    return render_template("thanks.html")


    
