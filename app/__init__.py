from flask import Flask, session, request, jsonify
from apispec import APISpec
from flask_restful import Api
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_session import Session

"""
Initialiasing application instance with Flask Framework and applying secret key to the application
"""
application = Flask(__name__)
application.secret_key = 'quiz-portal-12345'
# application.run(debug=True)
"""
Thsi will configure the swagger docs for the application
"""
from app.models import *

application.config['SESSION_TYPE'] = 'sqlalchemy'
application.config['SESSION_SQLALCHEMY_TABLE'] = 'user_session'
application.config['SESSION_SQLALCHEMY'] = db

sess = Session(application)
api = Api(application)  # Flask restful wraps Flask app around it.

# db.create_all()

application.config.update({
    'APISPEC_SPEC': APISpec(
        title='Quiz Portal',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(application)


# try:
#     add_questions()
# except Exception as e:
#     print(str(e))