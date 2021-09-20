# 作者：我只是代码的搬运工
# coding:utf-8
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

# 创建sqlalchemy对象
from flask_wtf import CSRFProtect

db = SQLAlchemy()
# 创建Bootstrap
bootstrap = Bootstrap()
# 创建本地化时间与日期
moment = Moment()
# 富文本编辑器
ckeditor = CKEditor()
# 电子邮件
mail = Mail()
# flask-login的使用
login_manager = LoginManager()
# debug管理
toolbar = DebugToolbarExtension()
# csrf认证
csrf = CSRFProtect()


# 用户加载函数,判断当前是否登录,用于current_user
@login_manager.user_loader
def load_user(user_id):
    from bluelog.models import Admin
    user = Admin.query.get(int(user_id))
    return user


# 当需要登录的路由退出登录时产生的警告
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录!'
login_manager.login_message_category = 'warning'
