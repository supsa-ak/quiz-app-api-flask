
# Quiz API
## Installation
Just follow this steps to run locally

Clone this project in your directory

```bash
git clone https://github.com/supsa-ak/quiz-app-api-flask.git
```
    
Go to "quiz-app-api-flask" folder
```bash
cd \quiz-app-api-flask\
```

Create Virtual Environment
```bash
virtualenv env
```

Activate Virtual Environment
```bash
.\env\Scripts\activate
```

Install neccessary libraries and packages
```bash
pip install -r requirements.txt
```

Run main.py file
```bash
python main.py
```
Development server will start at http://127.0.0.1:8000/

## API Reference

#### 1. SignUp User/Admin

```http
  POST /signup
```
Users will be signed up for using the application. Users will be Admin or Normal
Users.

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | **Required**. Name of User |
| `username` | `string` | **Required**. Username of User |
| `password` | `string` | **Required**. Password of User |
| `is_admin` | `integer` | **Required**. Admin status: 0 not admin, 1 admin |

SAMPLE JSON REQUEST FORMAT
```Json Format
{
    "name":"sak",
    "username":"sak",
    "password":"123",
    "is_admin":1
}
```
SAMPLE JSON RESPONSE FORMAT

Success
```Json Format
{"message": 'User created with name sak'}
```
Error
```Json Format
{'message': 'Something went wrong'}
```

#### 2. Login

```http
  POST /login
```
User can be able to login using the credentials. In this session_id will be created
which will be further used for all subsequent activities.

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. Username created at signup |
| `password` | `string` | **Required**. Password created at signup |


SAMPLE JSON REQUEST FORMAT
```Json Format
{
    "username":"sak",
    "password":"123"
}
```
SAMPLE JSON RESPONSE FORMAT

Success
```Json Format
{"message": "Successfully Logged in as sak"}
```
```Json Format
{"message": "Already Logged in as sak"]}
```

Error
```Json Format
{"message": "Incorrect Username or Password"}
```

#### 3. Logout

```http
  GET  /logout
  POST /logout
```
User will be perform a logout action in case of taking break from the application

SAMPLE JSON RESPONSE FORMAT

```Json Format
{"message":"User Logged Out"}
```

#### 4. Add Question

```http
  POST /add.question
```
 Admin can add new questions in the questions table.


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `question`| `string` | **Required**. Question statement |
| `choice1` | `string` | **Required**. Option 1 |
| `choice2` | `string` | **Required**. Option 2  |
| `choice3` | `string` | **Required**. Option 3   |
| `choice4` | `string` | **Required**. Option 4   |
| `answer` | `integer` | **Required**. Correct option no.|
| `marks` | `integer` | **Required**.  Marks |
| `remarks` | `string` | **Required**. About question|

SAMPLE JSON REQUEST FORMAT
```Json Format
{
    "question":"what is computer",
    "choice1":"machine",
    "choice2":"car",
    "choice3":"animal",
    "choice4":"plant",
    "answer":1,
    "marks":5,
    "remarks":"computer is machine"
}
```
SAMPLE JSON RESPONSE FORMAT

Success
```Json Format
{"message": "Question added Successfully"}
```

Error
```Json Format
{"message": "Don\'t have required privileges"}
```



#### 5. List All Questions

```http
  GET /list.questions
```
Admin can list all questions persisted in the database

SAMPLE JSON RESPONSE FORMAT

Success
```Json Format
[
    {
        "answer": 4,
        "choice1": "20",
        "choice2": "21",
        "choice3": "22",
        "choice4": "23",
        "created_ts": "Sun, 02 Jan 2022 08:38:54 GMT",
        "marks": 5,
        "question": "What is a+b if a = 4 and b = 19?",
        "question_id": 1,
        "remarks": "Additon Question",
        "updated_ts": null
    },
    {
        "answer": 2,
        "choice1": "3",
        "choice2": "4",
        "choice3": "5",
        "choice4": "6",
        "created_ts": "Sun, 02 Jan 2022 08:38:54 GMT",
        "marks": 5,
        "question": "If x = 9 and y = 5, that what is x-y?",
        "question_id": 2,
        "remarks": "Subtraction Question",
        "updated_ts": null
    }
]
```

Error
```Json Format
{"message": "Don\'t have required privileges"}
```


#### 6. Creating Quiz

```http
  POST /create.quiz
```
Admin can create a new quiz and tag the required questions to the created
quiz

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `quiz name`| `string` | **Required**. Set name of quiz|
| `question_id`| `integer` | **Required**. List of question ID|

SAMPLE JSON REQUEST FORMAT
```Json Format
{
    "quiz_name":"quiz name one",
    "question_id":[
        2,
        3,
        4,
        6
    ]
}
```
SAMPLE JSON RESPONSE FORMAT

Success
```Json Format
 {"message": "Quiz created successfully"}
```

Error
```Json Format
{"message": "Don\'t have required privileges"}
```



#### 7.  Assigning Quiz to Users 

```http
  POST /assign.quiz
```
Admin can assign the required quiz to the user.


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `user_id`| `integer` | **Required**. List of user id|
| `quiz_id`| `integer` | **Required**. List of quiz id|

SAMPLE JSON REQUEST FORMAT
```Json Format
{
    "user_id":[2,3],
    "quiz_id":[1,2]
}
```
SAMPLE JSON RESPONSE FORMAT

Success
```Json Format
{"message": "Quiz Assigned successfully"}
```

Error
```Json Format
{"message": "Don\'t have required privileges"}
```



#### 8. View quiz

```http
  POST /view.quiz
```
 Users are able to view the list of all questions for the particular quiz id.


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `quiz_id`| `integer` | **Required**. Quiz id of particular quiz assigned|

SAMPLE JSON REQUEST FORMAT
```Json Format
{
    "quiz_id":1
}
```
SAMPLE JSON RESPONSE FORMAT

Success
```Json Format
{
    "Quiz Name": "quiz name one",
    "Quiz Questions": [
        {
            "choice1": "3",
            "choice2": "4",
            "choice3": "5",
            "choice4": "6",
            "marks": 5,
            "question": "If x = 9 and y = 5, that what is x-y?",
            "question_id": 2
        },
        {
            "choice1": "12",
            "choice2": "13",
            "choice3": "15",
            "choice4": "16",
            "marks": 5,
            "question": "If in square, length of a side is 4, then what is the perimeter of the square?",
            "question_id": 3
        },
        {
            "choice1": "13",
            "choice2": "16",
            "choice3": "15",
            "choice4": "12",
            "marks": 5,
            "question": "If in square, length of a side is 4, then what is the area of the square?",
            "question_id": 4
        },
        {
            "choice1": "22",
            "choice2": "24",
            "choice3": "25",
            "choice4": "26",
            "marks": 5,
            "question": "What is a+b if a = 5 and b = 19?",
            "question_id": 6
        }
    ],
    "quiz_id": 1
}
```

Error
```Json Format
{"message": "This quiz is not assigned to you"}
```



#### 9.  List all Assigned Quizzes

```http
  GET /assigned.quizzes
```
Users can able to view the list of all assigned quizzes with the
respective status and with respective scores (submitted/not submitted)

SAMPLE JSON RESPONSE FORMAT

Success
```Json Format
{
    "Assigned Quizes": [
        {
            "is_submitted": "yes",
            "quiz_id": "1",
            "quiz_name": "quiz name one",
            "score_achieved": 10
        },
        {
            "is_submitted": "no",
            "quiz_id": "2",
            "quiz_name": "quiz name two",
            "score_achieved": null
        }
    ]
}
```

Error
```Json Format
{"message": "Quiz not Assigned"}
```



#### 10. List All Quizzes

```http
  GET /all.quizzes
```
 Admin can list all created quizzes.

SAMPLE JSON RESPONSE FORMAT

Success
```Json Format
[
    {
        "created_ts": "Sun, 02 Jan 2022 11:24:13 GMT",
        "quiz_id": 1,
        "quiz_name": "quiz name one",
        "updated_ts": "Sun, 02 Jan 2022 11:24:13 GMT"
    },
    {
        "created_ts": "Sun, 02 Jan 2022 11:31:36 GMT",
        "quiz_id": 2,
        "quiz_name": "quiz name two",
        "updated_ts": "Sun, 02 Jan 2022 11:31:36 GMT"
    }
]
```

Error
```Json Format
{"message": "Don\'t have required privileges"}
```



#### 11. Attempt Quiz

```http
  POST /attempt.quiz
```
Users can attempt the assigned quiz only once by submitting the
responses in the given json format. Response will be the score achieved from the quiz


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `quiz_id`| `integer` | **Required**. Quiz id of particular quiz assigned|
| `quiz_answers`| `string` | **Required**. List of question answer dictionaries|
| `question_id`| `integer` | **Required**. Question id of assigned question|
| `answer`| `integer` | **Required**. Attempted answer choice of question|

SAMPLE JSON REQUEST FORMAT
```Json Format
{
    "quiz_id":1,
    "quiz_answers":[
        {"question_id":2,"answer":2},
        {"question_id":3,"answer":4},
        {"question_id":4,"answer":3},
        {"question_id":6,"answer":3}
    ]
}
```
SAMPLE JSON RESPONSE FORMAT

Success
```Json Format
{"total_marks": 10, "message":"Quiz Submitted Successfully"}
```

Error
```Json Format
{"message": "This quiz is not assigned to you"}
```
```Json Format
 {"message": "Quiz is already Submitted"}
```


#### 12. Quiz Results

```http
  POST /quiz.results
```
 For a given quiz id, Admin can fetch quiz results in which the results are
sorted in decreasing order of the achieved scores and the quiz instances where users are
yet to attempt the quiz, will be displayed at last.


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `quiz_id`| `integer` | **Required**. Quiz id of particular quiz result|


SAMPLE JSON REQUEST FORMAT
```Json Format
{
    "quiz_id":1
}
```
SAMPLE JSON RESPONSE FORMAT

Success
```Json Format
{
    "Quiz Name": "quiz name one",
    "Quiz Results": [
        {
            "is_submitted": 1,
            "score_achieved": 10,
            "user_id": "2"
        },
        {
            "is_submitted": 0,
            "score_achieved": null,
            "user_id": "3"
        }
    ]
}
```

Error
```Json Format
{"message": "Don\'t have required privileges"}
```