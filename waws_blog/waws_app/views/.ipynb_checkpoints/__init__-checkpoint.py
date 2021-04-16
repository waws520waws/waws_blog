from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditor, CKEditorField
import pymysql


class mysql_conn(object):
    def __init__(self):
        self.conn = pymysql.connect(host="localhost",
                                    port=3306,
                                    user='root',
                                    password="111111",
                                    db='blog',
                                    charset='utf8mb4')
        # 创建一个游标
        self.cursor = self.conn.cursor()

class PostForm(FlaskForm):
    title = StringField('Title')
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')

mysql_ = mysql_conn()