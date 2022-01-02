from app.models import *
from app import *
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.extension import FlaskApiSpec
from sqlalchemy import desc
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
            return {"message": 'User created with name '+request.json['name']}, 201
        except:
            return {'message': 'Something went wrong'}

api.add_resource(SignUpAPI, '/signup')
docs.register(SignUpAPI)
"""JSON FORMAT
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
"""JSON FORMAT
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
"""JSON FORMAT
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
"""JSON FORMAT
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
    def post(self):
        if session['username']:
            pass
        else:
            return {"message": 'Login Required'}
        uname = session['username'] 
        user_info = UserMaster.query.filter_by(username=uname).first()
        if user_info.is_admin == 1:
            for i in request.json['quiz_id']:
                for j in request.json['user_id']:
                    q = QuizInstance(quiz_id=i, user_id=j, is_active=1, score_achieved=None, is_submitted=0)
                    db.session.add(q)
            db.session.commit()
            return  {"message": 'Quiz Assigned successfully'}, 200
        else:
            return {"message": 'Don\'t have required privileges'}, 404

api.add_resource(AssignQuizAPI, '/assign.quiz')
docs.register(AssignQuizAPI)
"""JSON FORMAT
{
    "user_id":[2,3],
    "quiz_id":[1,2]
}
"""
"""
[View Quiz API] : Its responsibility is to view the quiz details.
Only Admin and the assigned users to this quiz can access the quiz details.
"""
class ViewQuizAPI(MethodResource, Resource):
    def post(self):
        if session['username']:
            pass
        else:
            return {"message": 'Login Required'}
        user_id = UserMaster.query.filter_by(username=session['username']).first().user_id
        li = []
        li = QuizInstance.query.filter_by(user_id=user_id)
        Flag = False
        for i in li:
            if int(i.quiz_id) == request.json['quiz_id']:
                Flag = True 
                break 
        if Flag == True:
            quiz_name = QuizMaster.query.filter_by(quiz_id=request.json['quiz_id']).first().quiz_name
            li_1 = QuizQuestions.query.filter_by(quiz_id=request.json['quiz_id'])
            li_2 = []
            for i in li_1:
                li_2.append(i.question_id)
            params = []
            for j in li_2:
                m = QuestionMaster.query.filter_by(question_id=j).first() 
                question_info = {"question_id":m.question_id, "question":m.question, "choice1":m.choice1, "choice2":m.choice2, "choice3":m.choice3, "choice4":m.choice4, "marks":m.marks}
                
                params.append(question_info) 
            return {"quiz_id":request.json['quiz_id'], "Quiz Name":quiz_name, "Quiz Questions":params}, 200
        else: 
            return {"message": 'This quiz is not assigned to you'}, 404

api.add_resource(ViewQuizAPI, '/view.quiz')
docs.register(ViewQuizAPI)
"""JSON FORMAT
{
    "quiz_id":1
}
"""
"""
[View Assigned Quiz API] : Its responsibility is to list all the assigned quizzes 
                            with there submittion status and achieved scores.
"""
class ViewAssignedQuizAPI(MethodResource, Resource):
    def get(self):
        if session['username']:
            pass
        else:
            return {"message": 'Login Required'}
        user_id = UserMaster.query.filter_by(username=session['username']).first().user_id
        l = QuizInstance.query.filter_by(user_id=user_id)
        params = []
        
        for i in l:
            quiz_name = QuizMaster.query.filter_by(quiz_id=i.quiz_id).first().quiz_name
            if i.is_submitted == 0:
                submitted = 'no'
            else:
                submitted = 'yes'
            quiz = {"quiz_id":i.quiz_id, "quiz_name":quiz_name, "score_achieved":i.score_achieved, "is_submitted":submitted}
            params.append(quiz)

        if len(params) == 0:
            return {"message": "Quiz not Assigned"}, 404
        return {"Assigned Quizes":params}, 200
api.add_resource(ViewAssignedQuizAPI, '/assigned.quizzes')
docs.register(ViewAssignedQuizAPI)


"""
[View All Quiz API] : Its responsibility is to list all the created quizzes. Admin can only list all quizzes.
"""
class ViewAllQuizAPI(MethodResource, Resource):
    def get(self):
        if session['username']:
            pass
        else:
            return {"message": 'Login Required'}
        uname = session['username'] 
        user_info = UserMaster.query.filter_by(username=uname).first()
        if user_info.is_admin == 1:
            quizes = QuizMaster.query.all()
            params = []
            for i in quizes:
                q_info = {"quiz_id":i.quiz_id, "quiz_name":i.quiz_name,"created_ts":i.created_ts,"updated_ts":i.updated_ts}
                params.append(q_info)
            return params, 200
        else:
            return {"message": 'Don\'t have required privileges'}, 404


api.add_resource(ViewAllQuizAPI, '/all.quizzes')
docs.register(ViewAllQuizAPI)

"""
[Attempt Quiz API] : Its responsibility is to perform quiz attempt activity by 
                        the user and the score will be shown as a result of the submitted attempt.
"""
class AttemptQuizAPI(MethodResource, Resource):
    def post(self):
        if session['username']:
            pass
        else:
            return {"message": 'Login Required'}
        user_id = UserMaster.query.filter_by(username=session['username']).first().user_id
        
        li = QuizInstance.query.filter_by(user_id=str(user_id), quiz_id=str(request.json['quiz_id'])).first()
        Flag = False 
        if (int(li.quiz_id) == int(request.json['quiz_id'])) and (int(user_id) == int(li.user_id)):
            if li.is_submitted == 0:
                Flag = True 
            else:
                return  {"message": 'Quiz is already Submitted'}, 404
        else:
            return {"message": 'This quiz is not assigned to you'}, 404
        if Flag == True:
            total_marks = 0
            for i in request.json['quiz_answers']:
                c = UserResponses(quiz_id=request.json['quiz_id'], user_id=user_id, question_id=i['question_id'], response=i['answer'], is_active=1)
                db.session.add(c)
                if QuestionMaster.query.filter_by(question_id=i['question_id']).first().answer == i['answer']:
                    total_marks += QuestionMaster.query.filter_by(question_id=i['question_id']).first().marks
            li.score_achieved = total_marks
            li.is_submitted = 1
            db.session.commit()
            return {"total_marks": total_marks, "message":"Quiz Submitted Successfully"}

api.add_resource(AttemptQuizAPI, '/attempt.quiz')
docs.register(AttemptQuizAPI)
"""JSON FORMAT
{
    "quiz_id":1,
    "quiz_answers":[
        {"question_id":2,"answer":2},
        {"question_id":3,"answer":4},
        {"question_id":4,"answer":3},
        {"question_id":6,"answer":3}
    ]
}
"""
"""
[Quiz Results API] : Its responsibility is to provide the quiz results in which the users 
                        having the scores sorted in descending order are displayed, 
                        also the ones who have not attempted are also shown.
                        Admin has only acess to this functionality.
"""
class QuizResultAPI(MethodResource, Resource):
    def post(self):
        if session['username']:
            pass
        else:
            return {"message": 'Login Required'}
        uname = session['username'] 
        user_info = UserMaster.query.filter_by(username=uname).first()
        if user_info.is_admin == 1:
            quiz_name = QuizMaster.query.filter_by(quiz_id=request.json['quiz_id']).first().quiz_name
            quiz_intstances = QuizInstance.query.filter_by(quiz_id=str(request.json['quiz_id'])).order_by(desc(QuizInstance.score_achieved))
            li = []
            for i in quiz_intstances:
                instace_info = {"user_id":i.user_id, "is_submitted":i.is_submitted, "score_achieved":i.score_achieved}
                li.append(instace_info)
            return {"Quiz Name":quiz_name, "Quiz Results":li}, 200
        else:
            return {"message": 'Don\'t have required privileges'}, 404

api.add_resource(QuizResultAPI, '/quiz.results')
docs.register(QuizResultAPI)
"""JSON FORMAT
{
    "quiz_id":1
}
"""