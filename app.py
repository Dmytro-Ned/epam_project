from src import db, instantiate_app
from src.auth.models import User
from src.posts.models import Post
from src.quiz.models import Option, Result, Test, Question


app = instantiate_app()


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Option": Option, "Post": Post, "Result": Result,
            "Test": Test, "Question": Question, "User": User}


if __name__ == "__main__":
    app.run(debug=True, port=2021)
