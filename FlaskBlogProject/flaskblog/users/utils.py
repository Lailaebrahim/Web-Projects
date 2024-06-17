import secrets
import os
from PIL import Image
from flask import url_for, current_app
from flaskblog import mail
from flask_login import current_user
from flask_mail import Message


# Method to save profile pics as static files and return the path of image
def savr_pic(form_profile_pic):
    # creating a random hex token to name the image so pathes saved in DB don't repeat
    random_hex = secrets.token_hex(8)
    # using os.path methods to get the extension of the uploaded image
    _, fext = os.path.splitext(form_profile_pic.filename)
    # profile picture file name is the generasted randon hex token and the extension
    pic_name = random_hex + fext
    # creating the full path of the profile picture so it can be used to be rendered by templates
    pic_path = os.path.join(current_app
                            .root_path, 'static/profile_pics', pic_name)
    # Resizing image so it want take up much space
    input_size = (125, 125)
    i = Image.open(form_profile_pic)
    i.thumbnail(input_size)
    i.save(pic_path)
    if current_user.image_file != None:
        # deleting the old image from the static folder
        os.remove(os.path.join(current_app
                               .root_path, 'static/profile_pics', current_user.image_file))
    return pic_name


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset', recipients=[
                  user.email], sender='lailaebrahimtawfik@gmail.com')
    msg.body = f"To Reset Your Password visit the following link {
        url_for('users.reset_password', token=token, _external=True)}"
    mail.send(msg)
