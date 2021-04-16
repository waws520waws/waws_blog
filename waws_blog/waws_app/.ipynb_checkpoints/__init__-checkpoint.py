from flask import Flask
from .views.blog import blog_blueprint
from .views.admin import admin_blueprint
from . import config
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditor, CKEditorField

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(blog_blueprint)
    app.register_blueprint(admin_blueprint)
    app.secret_key = 'secret string'
    ckeditor = CKEditor(app)
    return app

class PostForm(FlaskForm):
    title = StringField('Title')
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')

