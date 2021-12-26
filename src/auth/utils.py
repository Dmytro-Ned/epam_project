import os
import secrets
from threading import Thread
#
from flask import current_app, render_template
from flask_login import current_user
from flask_mail import Message
from PIL import Image
#
from src import mail


def save_image(image_data):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(image_data.filename)
    filename = random_hex + file_ext
    image_path = os.path.join(current_app.root_path, 'static/avatars', filename)  # TODO: fix
    if not current_user.image.startswith("default.png"):
        os.remove(os.path.join(current_app.root_path, 'static/avatars', current_user.image))
    output_size = 200, 200
    avatar = Image.open(image_data)
    avatar.thumbnail(output_size)
    avatar.save(image_path)
    return filename


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_reset_email(user):
    token = user.get_reset_token()  # accepts secs_to_expire
    msg = Message(subject="[SnakeTests] Password reset request",
                  sender="snaketests.app@gmail.com@gmail.com",
                  recipients=[user.email])
    msg.html = render_template('auth/reset_letter.html',
                               user=user, token=token)
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
