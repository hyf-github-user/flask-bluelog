# 作者：我只是代码的搬运工
# coding:utf-8
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm

from wtforms import StringField, BooleanField, SubmitField, TextAreaField, HiddenField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, Optional, Email, URL

# 自定义表单
from bluelog import Category


# 方便出现中文调试信息
class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['zh']


# 登录表单
class LoginForm(MyBaseForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = StringField('Password', validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


# 文章表单
class PostForm(MyBaseForm):
    title = StringField('主题', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('分类', coerce=int, default=1)
    body = CKEditorField('内容', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]


# 分类表单
class CategoryForm(MyBaseForm):
    name = StringField('名称', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use.')


# 评论表单
class CommentForm(FlaskForm):
    author = StringField('用户名', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    site = StringField('地区', validators=[Optional(), URL(), Length(0, 255)])
    body = TextAreaField('评论', validators=[DataRequired()])
    submit = SubmitField()


# 针对管理员的评论
class AdminCommentForm(CommentForm):
    author = HiddenField()  # 对应HTML <input type="hidden">
    email = HiddenField()
    site = HiddenField()
