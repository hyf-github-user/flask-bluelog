# 作者：我只是代码的搬运工
# coding:utf-8
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm

from wtforms import StringField, BooleanField, SubmitField, TextAreaField, HiddenField, SelectField, PasswordField, \
    ValidationError
from wtforms.validators import DataRequired, Length, Optional, Email, URL

# 自定义表单


from bluelog.models import Category


# 方便出现中文调试信息
class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['zh']


# 登录表单
class LoginForm(MyBaseForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')


# 文章表单
class PostForm(MyBaseForm):
    title = StringField('主题', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('分类', coerce=int, default=1)
    body = CKEditorField('内容', validators=[DataRequired()])
    submit = SubmitField('发布')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]


# 分类表单
class CategoryForm(FlaskForm):
    name = StringField('名称', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('分类已被创建!')


# 评论表单
class CommentForm(MyBaseForm):
    author = StringField('用户名', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    site = StringField('地区', validators=[Optional(), URL(), Length(0, 255)])
    body = TextAreaField('评论', validators=[DataRequired()])
    submit = SubmitField('发布')


# 设置表单
class SettingForm(MyBaseForm):
    name = StringField('姓名', validators=[DataRequired(), Length(1, 30)])
    blog_title = StringField('大标题', validators=[DataRequired(), Length(1, 60)])
    blog_sub_title = StringField('小标题', validators=[DataRequired(), Length(1, 100)])
    about = CKEditorField('关于我', validators=[DataRequired()])
    submit = SubmitField('更新')


# 针对管理员的评论
class AdminCommentForm(CommentForm):
    author = HiddenField()  # 对应HTML <input type="hidden">
    email = HiddenField()
    site = HiddenField()


# 友情链接表单
class LinkForm(FlaskForm):
    name = StringField('名称', validators=[DataRequired(), Length(1, 30)])
    url = StringField('网址', validators=[DataRequired(), URL(), Length(1, 255)])
    submit = SubmitField()
