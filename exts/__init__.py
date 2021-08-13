# 作者：我只是代码的搬运工
# coding:utf-8
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

# 创建sqlalchemy对象
db = SQLAlchemy()
# 创建Bootstrap
bootstrap = Bootstrap()
# 创建本地化时间与日期
moment = Moment()
# 富文本编辑器
ckeditor = CKEditor()
# 电子邮件
mail = Mail()
