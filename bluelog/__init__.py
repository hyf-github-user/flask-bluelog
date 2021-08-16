# 作者：我只是代码的搬运工
# coding:utf-8
from flask import Flask

from bluelog.blueprints.admin import admin_bp
from bluelog.blueprints.auth import auth_bp
from bluelog.blueprints.blog import blog_bp
from exts import db, bootstrap, mail, ckeditor, moment
from settings import DevelopmentConfig


def create_app():
    app = Flask('bluelog', template_folder='../templates', static_folder='../static')
    app.config.from_object(DevelopmentConfig)
    # 初始化扩展
    register_extensions(app)
    # 注册蓝图
    register_blueprints(app)
    return app


# 初始化扩展
def register_extensions(app):
    # 初始化db
    db.init_app(app=app)
    # 初始化Bootstrap
    bootstrap.init_app(app=app)
    # 初始化邮箱
    mail.init_app(app=app)
    # 富文本编辑器
    ckeditor.init_app(app=app)
    # 初始化时间与日期
    moment.init_app(app=app)


# 注册蓝图
def register_blueprints(app):
    # 注册蓝图
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
