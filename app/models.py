from enum import unique
from marshmallow.schema import Schema
from sqlalchemy.orm import session
from app import application
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# import uuid

"""
[DataBase Access Details]
Below is the configuration mentioned by which the application can make connection with MySQL database
"""
# username = 'root'
# word = 'root'
# database_name = 'quiz_app'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///..\db.sqlite3'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(application)

class UserMaster(db.Model):
        __tablename__ = 'user_master'
        user_id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(200))
        username = db.Column(db.String(200))
        password = db.Column(db.String(200))
        is_admin = db.Column(db.Integer)
        is_active = db.Column(db.Integer)
        created_ts = db.Column(db.DateTime, default=db.func.current_timestamp())
        updated_ts = db.Column(db.DateTime, default=db.func.now(), server_onupdate=db.func.now())

        def __init__(self, name, username, password, is_admin, is_active):
                self.name = name
                self.username = username
                self.password = password
                self.is_admin = is_admin   
                self.is_active = is_active  

class QuestionMaster(db.Model):
        __tablename__ = 'question_master'
        question_id = db.Column(db.Integer, primary_key=True)
        question = db.Column(db.String(500))
        choice1 = db.Column(db.String(500))
        choice2 = db.Column(db.String(500))
        choice3 = db.Column(db.String(500))
        choice4 = db.Column(db.String(500))
        answer = db.Column(db.Integer)
        marks = db.Column(db.Integer)
        remarks = db.Column(db.String(200))
        is_active = db.Column(db.Integer)
        created_ts = db.Column(db.DateTime, default=db.func.current_timestamp())
        updated_ts = db.Column(db.DateTime, default=db.func.now(), server_onupdate=db.func.now())

        def __init__(self, question, choice1, choice2, choice3, choice4, answer, marks, remarks):
                self.question = question
                self.choice1 = choice1
                self.choice2 = choice2
                self.choice3 = choice3
                self.choice4 = choice4
                self.answer = answer
                self.marks = marks
                self.remarks = remarks
            
class QuizMaster(db.Model):
        __tablename__ = 'quiz_master'
        quiz_id = db.Column(db.Integer, primary_key=True)
        quiz_name = db.Column(db.String(100))
        is_active = db.Column(db.Integer)
        created_ts = db.Column(db.DateTime, default=db.func.current_timestamp())
        updated_ts = db.Column(db.DateTime, default=db.func.now(), server_onupdate=db.func.now())
        
        def __init__(self, quiz_name,  is_active):
                self.quiz_name = quiz_name
                self.is_active = is_active
            
class QuizQuestions(db.Model):
        __tablename__ = 'quiz_questions'
        __table_args__ = (
                db.UniqueConstraint('quiz_id', 'question_id', name='unique_quiz_question'),
        )
        id = db.Column(db.Integer, primary_key=True)
        quiz_id = db.Column(db.String(200), db.ForeignKey("quiz_master.quiz_id"))
        question_id = db.Column(db.String(200), db.ForeignKey("question_master.question_id"))
        is_active = db.Column(db.Integer)
        created_ts = db.Column(db.DateTime, default=db.func.current_timestamp())
        updated_ts = db.Column(db.DateTime, default=db.func.now(), server_onupdate=db.func.now())

        def __init__(self, quiz_id, question_id, is_active):
                self.quiz_id = quiz_id
                self.question_id = question_id
                self.is_active = is_active
     
class QuizInstance(db.Model):
        __tablename__ = 'quiz_instance'
        __table_args__ = (
                db.UniqueConstraint('quiz_id', 'user_id', name='unique_quiz_user'),
        )
        id = db.Column(db.Integer, primary_key=True)
        quiz_id = db.Column(db.String(200), db.ForeignKey("quiz_master.quiz_id"))
        user_id = db.Column(db.String(200), db.ForeignKey("user_master.user_id"))
        score_achieved = db.Column(db.Integer)
        is_submitted = db.Column(db.Integer)
        is_active = db.Column(db.Integer)
        created_ts = db.Column(db.DateTime, default=db.func.current_timestamp())
        updated_ts = db.Column(db.DateTime, default=db.func.now(), server_onupdate=db.func.now())
        
        def __init__(self, quiz_id, user_id):
                self.quiz_id = quiz_id
                self.user_id = user_id
            
class UserResponses(db.Model):
        __tablename__ = 'user_responses'
        __table_args__ = (
                db.UniqueConstraint('quiz_id', 'user_id', 'question_id', name='unique_quiz_user_question'),
        )
        id = db.Column(db.Integer, primary_key=True)
        quiz_id = db.Column(db.String(200), db.ForeignKey("quiz_master.quiz_id"))
        user_id = db.Column(db.String(200), db.ForeignKey("user_master.user_id"))
        question_id = db.Column(db.String(200), db.ForeignKey("question_master.question_id"))
        response = db.Column(db.Integer)
        is_active = db.Column(db.Integer)
        created_ts = db.Column(db.DateTime, default=db.func.current_timestamp())
        updated_ts = db.Column(db.DateTime, default=db.func.current_timestamp(), server_onupdate=db.func.current_timestamp())

        def __init__(self, quiz_id, user_id, question_id, response):
                self.quiz_id = quiz_id
                self.user_id = user_id
                self.question_id = question_id
                self.response = response        
    
db.create_all()
db.session.commit()