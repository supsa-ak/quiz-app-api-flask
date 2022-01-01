from enum import unique
from marshmallow.schema import Schema
from sqlalchemy.orm import session
from app import application
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
        user_id = db.Column(db.String(200), primary_key=True)
        name = v
        username = db.Column(db.String(200))
        word = db.Column(db.String(200))
        is_admin = db.Column(db.Integer)
        is_active = db.Column(db.Integer)
        created_ts = db.Column(db.DateTime, default=db.func.current_timestamp())
        updated_ts = db.Column(db.DateTime)

        def __init__(self, id, name, username, word, is_admin):
            
            
class UserSession(db.Model):
        __tablename__ = 'user_session'
        id = db.Column(db.String(200), primary_key=True)
        user_id = db.Column(db.String(200), db.ForeignKey("user_master.user_id"))
        session_id = db.Column(db.String(200))
        is_active = db.Column(db.Integer)
        created_ts = db.Column(db.DateTime, default=db.func.current_timestamp())
        updated_ts = db.Column(db.DateTime)

        def __init__(self, id, user_id, session_id):

class QuestionMaster(db.Model):
        __tablename__ = 'question_master'
        question_id = db.Column(db.String(100), primary_key=True)
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
        updated_ts = db.Column(db.DateTime)

        def __init__(self, id, question, choice1, 
                     choice2, choice3, choice4, answer, marks, remarks):

            
class QuizMaster(db.Model):
        __tablename__ = 'quiz_master'
        quiz_id = 
        
        
        def __init__(self, id, quiz_name):
            
            
class QuizQuestions(db.Model):
        
        __tablename__ = 'quiz_questions'
        __table_args__ = (
                db.UniqueConstraint('quiz_id', 'question_id', name='unique_quiz_question'),
        )
        
        
        
        def __init__(self, id, quiz_id, question_id):
            
     
class QuizInstance(db.Model):
        __tablename__ = 'quiz_instance'
        __table_args__ = (
                db.UniqueConstraint('quiz_id', 'user_id', name='unique_quiz_user'),
        )
        
        
        
        def __init__(self, id, quiz_id, user_id):
            
            
class UserResponses(db.Model):
        __tablename__ = 'user_responses'
        __table_args__ = (
                db.UniqueConstraint('quiz_id', 'user_id', 'question_id', name='unique_quiz_user_question'),
        )
        
        
        
        def __init__(self, id, quiz_id, user_id, question_id, response):
            
        
    
db.create_all()
db.session.commit()