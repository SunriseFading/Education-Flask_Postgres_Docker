
from datetime import datetime
import datetime
import requests
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://test:test@localhost:5000/test"
db = SQLAlchemy(app)


class Answers(db.Model):
    __tablename__ = 'answers'
    primary_key = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, unique=True, nullable=False)
    question = db.Column(db.String(64), nullable=False)
    answer = db.Column(db.String(128), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, id, question, answer):
        self.id = id
        self.question = question
        self.answer = answer


with app.app_context():
    db.create_all()


def api_request(amount: str):
    link = 'https://jservice.io/api/random'
    params = {'count': amount}
    return requests.get(link, params=params).json()


def add_database(id: int, question: str, answer: str):
    while True:
        answer = Answers(id, question, answer)
        try:
            db.session.add(answer)
            db.session.commit()
        except Exception:
            data: list = api_request('1')
            add_database(data[0]['id'], data[0]['answer'], data[0]['question'])
        return


@app.route('/', methods=['POST'])
def test():
    questions_num = str(request.get_json()['questions_num'])
    data: list = api_request(questions_num)
    for unit in data:
        add_database(unit['id'], unit['question'],
                     unit['answer'])
    return 'Successful'
