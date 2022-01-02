from app.models import *
from app import *
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.extension import FlaskApiSpec
from app.schemas import *
from app.services import *
from datetime import datetime
import json 

"""
[Sign Up API] : Its responsibility is to perform the signup activity for the user.
"""
#  Restful way of creating APIs through Flask Restful
class SignUpAPI(MethodResource, Resource):
    def post(self):
        try:
            c = UserMaster(name=request.json['name'], username=request.json['username'], password=request.json['password'], is_admin=request.json['is_admin'], is_active=1)
            db.session.add(c)
            db.session.commit()
            return {"message": 'customer created with name '+request.json['name']}, 201
        except:
            return {'message': 'Something went wrong'}

api.add_resource(SignUpAPI, '/signup')
docs.register(SignUpAPI)
"""
{
    "name":"sak",
    "username":"sak",
    "password":"123",
    "is_admin":1
}
"""

"""
[Login API] : Its responsibility is to perform the login activity for the user and 
create session id which will be used for all subsequent operations.
"""
class LoginAPI(MethodResource, Resource):
    def post(self):
        try:
            if session['username']:
                pass
        except:
            session['username'] = ""

        if session['username']:
            return {"message": 'Already Logged in as '+ session['username']}, 200
        try:
            uname = request.json['username']
            pword = request.json['password']
            if UserMaster.query.filter_by(username=uname).first():
                stud = UserMaster.query.filter_by(username=uname).first()
                if UserMaster.query.get(stud.user_id).password == pword:
                    
                    session['username'] = uname
                    
                    return {"message": 'Successfully Logged in as '+ uname}, 201
                else:
                    return  {"message": 'Incorrect Username or Password'}, 404
            else:
                return  {"message": 'Incorrect Username or Password'}, 404
        except:
                return  {"message": 'Incorrect Username or Password'}, 404

api.add_resource(LoginAPI, '/login')
docs.register(LoginAPI)
"""
{
    "username":"sak",
    "password":"123"
}
"""
"""
[Logout API] : Its responsibility is to perform the logout activity for the user.
"""
class LogoutAPI(MethodResource, Resource):
    def get(self):      
        session['username'] = None
        return {"message":"User Logged Out"}
    def post(self):      
        session['username'] = None
        return {"message":"User Logged Out"}
            

api.add_resource(LogoutAPI, '/logout')
docs.register(LogoutAPI)

"""
[Add Question API] : Its responsibility is to add question to the question bank.
Admin has only the rights to perform this activity.
"""
class AddQuestionAPI(MethodResource, Resource):
    def post(self):
        if session['username']:
            pass
        else:
            return {"message": 'Login Required'}
        uname = session['username'] 
        user_info = UserMaster.query.filter_by(username=uname).first()
        if user_info.is_admin == 1:
            q = QuestionMaster(question=request.json['question'], choice1=request.json['choice1'], choice2=request.json['choice2'], choice3=request.json['choice3'], choice4=request.json['choice4'],answer=request.json['answer'],marks=request.json['marks'],remarks=request.json['remarks'])
            db.session.add(q)
            db.session.commit()
            return {"message": 'Question added Successfully'}, 201
        else:
            return {"message": 'Don\'t have required privileges'}, 404

api.add_resource(AddQuestionAPI, '/add.question')
docs.register(AddQuestionAPI)
"""
{
    "question":"what is computer",
    "choice1":"machine",
    "choice2":"car",
    "choice3":"animal",
    "choice4":"plant",
    "answer":"1",
    "marks":"5",
    "remarks":"computer is machine"
}
"""
"""
[List Questions API] : Its responsibility is to list all questions present activly in the question bank.
Here only Admin can access all the questions.
"""
class ListQuestionAPI(MethodResource, Resource):
    def get(self):
        if session['username']:
            pass
        else:
            return {"message": 'Login Required'}
        uname = session['username'] 
        user_info = UserMaster.query.filter_by(username=uname).first()
        if user_info.is_admin == 1:
            all_questions = QuestionMaster.query.all()
            params = []
            for i in all_questions:
                question_info = {"question_id":i.question_id, "question":i.question, "choice1":i.choice1, "choice2":i.choice2, "choice3":i.choice3, "choice4":i.choice4, "marks":i.marks, "answer":i.answer, "remarks":i.remarks, "created_ts":i.created_ts, "updated_ts":i.updated_ts}
                params.append(question_info)
            return params, 200
        else:
            return {"message": 'Don\'t have required privileges'}, 404


api.add_resource(ListQuestionAPI, '/list.questions')
docs.register(ListQuestionAPI)

"""
[Create Quiz API] : Its responsibility is to create quiz and only admin can create quiz using this API.
"""
class CreateQuizAPI(MethodResource, Resource):
    def post(self):
        if session['username']:
            pass
        else:
            return {"message": 'Login Required'}
        uname = session['username'] 
        user_info = UserMaster.query.filter_by(username=uname).first()
        if user_info.is_admin == 1:
            q = QuizMaster(quiz_name=request.json['quiz_name'], is_active=1)
            db.session.add(q)

            quiz_id = QuizMaster.query.filter_by(quiz_name=request.json['quiz_name']).first().quiz_id
            for i in request.json['question_id']:           
                p = QuizQuestions(quiz_id=quiz_id, question_id=i, is_active=1)
                db.session.add(p)
            
            db.session.commit()
            return  {"message": 'Quiz created successfully'}, 200
        else:
            return {"message": 'Don\'t have required privileges'}, 404

api.add_resource(CreateQuizAPI, '/create.quiz')
docs.register(CreateQuizAPI)
"""
{
    "quiz_name":"quiz name one",
    "question_id":[
        2,
        3,
        4,
        6
    ]
}
"""
"""
[Assign Quiz API] : Its responsibility is to assign quiz to the user. Only Admin can perform this API call.
"""
class AssignQuizAPI(MethodResource, Resource):
    pass


api.add_resource(AssignQuizAPI, '/assign.quiz')
docs.register(AssignQuizAPI)

"""
[View Quiz API] : Its responsibility is to view the quiz details.
Only Admin and the assigned users to this quiz can access the quiz details.
"""
class ViewQuizAPI(MethodResource, Resource):
    pass


api.add_resource(ViewQuizAPI, '/view.quiz')
docs.register(ViewQuizAPI)

"""
[View Assigned Quiz API] : Its responsibility is to list all the assigned quizzes 
                            with there submittion status and achieved scores.
"""
class ViewAssignedQuizAPI(MethodResource, Resource):
    pass


api.add_resource(ViewAssignedQuizAPI, '/assigned.quizzes')
docs.register(ViewAssignedQuizAPI)


"""
[View All Quiz API] : Its responsibility is to list all the created quizzes. Admin can only list all quizzes.
"""
class ViewAllQuizAPI(MethodResource, Resource):
    pass


api.add_resource(ViewAllQuizAPI, '/all.quizzes')
docs.register(ViewAllQuizAPI)

"""
[Attempt Quiz API] : Its responsibility is to perform quiz attempt activity by 
                        the user and the score will be shown as a result of the submitted attempt.
"""
class AttemptQuizAPI(MethodResource, Resource):
    pass


api.add_resource(AttemptQuizAPI, '/attempt.quiz')
docs.register(AttemptQuizAPI)

"""
[Quiz Results API] : Its responsibility is to provide the quiz results in which the users 
                        having the scores sorted in descending order are displayed, 
                        also the ones who have not attempted are also shown.
                        Admin has only acess to this functionality.
"""
class QuizResultAPI(MethodResource, Resource):
    pass


api.add_resource(QuizResultAPI, '/quiz.results')
docs.register(QuizResultAPI)


