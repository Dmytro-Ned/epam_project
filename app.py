"""
Main manager file (WSGI) of the project.
"""

from src import db, instantiate_app
from src.auth.models import User
from src.posts.models import Post
from src.quiz.models import Option, Result, Test, Question


app = instantiate_app()  # pylint: disable=C0103


@app.shell_context_processor
def make_shell_context():
    """
    Adds default identifiers to the "flask shell"
    :return dict: pairs of identifiers and objects they relate to
    """
    return {"db": db, "Option": Option, "Post": Post, "Result": Result,
            "Test": Test, "Question": Question, "User": User}


if __name__ == "__main__":
    app.run(debug=False, port=2022)

