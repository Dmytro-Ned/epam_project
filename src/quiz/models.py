"""
This module contains SQL ORM models for
"Test", "Question", "Options", "Result" instances.
"""

from enum import Enum
from uuid import uuid4
#
from flask import flash
from flask_login import current_user
from sqlalchemy.dialects.postgresql import UUID
#
from src import db


class Test(db.Model):
    """
    An ORM class which represents SQL table "test".

    Fields: id, uuid, title, description, level, image,
            related questions, related results, related posts

    class Level: Enum-based levels of the test

    Methods:
        - get_num_questions
        - get_best_result
        - get_last_result
    """

    class Level(Enum):
        """
        Class represent possible levels
        of difficulty of a test.
        """
        BASIC = "Basic"
        MIDDLE = "Middle"
        ADVANCED = "Advanced"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), default=uuid4, index=True, unique=True)  # PgSQL
    # uuid = db.Column(db.String(length=32), default=generate_uuid, index=True, unique=True) # SQLt
    title = db.Column(db.String(64), nullable=False, unique=False)
    description = db.Column(db.Text())
    level = db.Column(db.Enum(Level), default=Level.BASIC, nullable=False)
    image = db.Column(db.String(20), default='default_test.png', nullable=False, unique=False)
    questions = db.relationship('Question', backref='test', cascade="all, delete-orphan",
                                lazy=True, passive_deletes=True)
    results = db.relationship('Result', backref='test', cascade="all, delete-orphan",
                              lazy=True, passive_deletes=True)
    posts = db.relationship('Post', backref='test', cascade="all, delete-orphan",
                            lazy=True, passive_deletes=True)

    def get_num_questions(self):
        """
        Calculates the number of questions of the test

        :return int: the number of questions
        """
        return len(self.questions)

    def get_best_result(self):
        """
        Fetches the best result of the currently logged user
        for the current test.

        :return int: the maximal number of correct answers
        """
        user_specific_results = filter(lambda result: result.user_id == current_user.id,
                                       self.results)
        correct_answers = sorted(map(lambda result: result.num_correct_answers,
                                     user_specific_results))
        return max(correct_answers) if correct_answers else 0

    def get_last_result(self):
        """
        Fetches the last result of the currently logged user
        for the current test or an indicator of its absence.

        :return Result/bool: the last result of the current user/False flag
        """
        user_specific_results = filter(lambda result: result.user_id == current_user.id,
                                       self.results)
        unfinished_results = list(filter(lambda result: result.state == Result.State.NEW,
                                         user_specific_results))
        if unfinished_results:
            return unfinished_results[-1]
        return False

    def __repr__(self):
        """
        Readable representation of an instance.

        :return str: the id and the title of the test
        """
        return f"Test(id: #{self.id}, {self.title})"


class Question(db.Model):
    """
    An ORM class which represents SQL table "question".

    Fields: id, order number, text, related test, related options
    """
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.SmallInteger)
    text = db.Column(db.Text())
    test_id = db.Column(db.Integer, db.ForeignKey('test.id', ondelete="CASCADE"), nullable=False)
    options = db.relationship('Option', backref='question', cascade="all, delete-orphan",
                              lazy=True, passive_deletes=True)

    def __repr__(self):
        """
        Readable representation of an instance.

        :return str: the title of the related test and the order number of the question
        """
        return f'Question({self.test.title}: №{self.order_number})'


class Option(db.Model):
    """
    An ORM class which represents SQL table "option".

    Fields: id, text, flag of correctness, related question
    """
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text())
    is_correct = db.Column(db.Boolean, default=False, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete="CASCADE"),
                            nullable=False)

    def __repr__(self):
        """
        Readable representation of an instance.

        :return str: the id of the option, of its related question
                     and the order number of the related question
        """
        return f'Option(id:{self.id} to question id:' \
               f'{self.question_id} №{self.question.order_number})'


class Result(db.Model):
    """
    An ORM class which represents SQL table "result".

    Fields: id, uuid, state, text, last answered question, number of correct answers,
    number of incorrect answers, related user, related test
    """

    class State(Enum):
        """
        Class represent possible states
        of completeness of a test (result status).
        """
        NEW = "Unfinished"
        FINISHED = "Finished"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), default=uuid4, index=True, unique=True)
    state = db.Column(db.Enum(State), default=State.NEW, nullable=False)
    last_question = db.Column(db.SmallInteger, default=0)
    num_correct_answers = db.Column(db.SmallInteger, default=0)
    num_incorrect_answers = db.Column(db.SmallInteger, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id', ondelete="CASCADE"), nullable=False)

    def update_result(self, model_option):
        """
        Updates fields of the result as test completion proceeds.

        :param Option model_option: a selected by user option instance of a question
        """
        if model_option.is_correct:
            self.num_correct_answers += 1
            flash("Correct answer", category="info")
        else:
            self.num_incorrect_answers += 1
            flash("Wrong answer", category="danger")
        self.last_question += 1
        if self.last_question == self.test.get_num_questions():
            self.state = self.State.FINISHED
        db.session.commit()
