"""
The module renders backend view-functions' behavior
of the BP-registered application "posts"
during client-server interaction through HTML templates.
"""

from flask import abort, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
#
from src.main.service import session_create, session_update, session_delete
from src.posts import bp
from src.posts.models import Post
from src.quiz.models import Test
from src.posts.forms import PostForm


@bp.route("/posts/create", methods=["GET", "POST"])
@login_required
def post_create_page():
    """
    The function manages post creation procedure.

    :return str: an HTML template for home page/post page
    """
    form = PostForm()
    form.test.choices = [test.title for test in Test.query.all()]
    if form.validate_on_submit():
        test = Test.query.filter_by(title=form.test.data).first()  # tests may share similar name
        post = Post(title=form.title.data, content=form.content.data,
                    test_id=test.id, author=current_user)
        session_create(post)
        flash('Thank you fot the feedback', category="success")
        return redirect(url_for("main.home_page"))  # do not remove: POST-GET-redirect pattern
    return render_template("posts/post_create_or_update.html",
                           form=form,
                           operation="Create a new")


@bp.route("/posts", methods=["GET", "POST"])
@login_required
def post_list_view_page():
    """
    The function manages posts display procedure.

    :return str: an HTML template for posts (list) page
    """
    posts = Post.query.order_by(Post.post_date.desc()).paginate(
        per_page=current_app.config['POSTS_PER_PAGE']
    )
    return render_template("posts/post_list_view.html", posts=posts)


@bp.route("/posts/<uuid:post_uuid>", methods=["GET", "POST"])
@login_required
def post_update_page(post_uuid):
    """
    The function manages post update procedure.

    :param UUID post_uuid: the UUID of an instance of the "Post" ORM model
    :return str: an HTML template for posts (list) page/post page
    """
    post = Post.query.filter_by(uuid=post_uuid).first()
    if post.author != current_user:  # in case of attempt to change the post by another user
        abort(403)
    form = PostForm()
    form.test.choices = [test.title for test in Test.query.all()]
    if form.validate_on_submit():
        test = Test.query.filter_by(title=form.test.data).first()  # tests may share similar name
        post.test_id = test.id
        post.title = form.title.data
        post.content = form.content.data
        session_update()  # no 'db.session.add' is required when altering a table row
        flash("The post has been successfully updated", category="success")
        return redirect(url_for('posts.post_list_view_page', post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
        form.test.data = post.test.title
    return render_template("posts/post_create_or_update.html",
                           form=form,
                           operation="Update your",
                           post=post)


@bp.route("/posts/delete/<uuid:post_uuid>", methods=["POST"])  # no 'GET' template
@login_required
def post_delete(post_uuid):
    """
    The function manages post deletion procedure.

    :param UUID post_uuid: the UUID of an instance of the "Post" ORM model
    :return str: an HTML template for posts (list) page
    """
    post = Post.query.filter_by(uuid=post_uuid).first()
    if post.author != current_user:  # in case of attempt to change the post by another user
        abort(403)
    session_delete(post)
    flash("The post has been successfully deleted", category="success")
    return redirect(url_for("posts.post_list_view_page"))
