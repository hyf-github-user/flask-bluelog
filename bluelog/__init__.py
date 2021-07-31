# 作者：我只是代码的搬运工
# coding:utf-8
from flask import Flask

from exts import db
from settings import DevelopmentConfig


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(DevelopmentConfig)
    # 初始化db
    db.init_app(app=app)
    return app