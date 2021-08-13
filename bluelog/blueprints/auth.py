# 作者：我只是代码的搬运工
# coding:utf-8
from flask import Blueprint

# 创建一个用户认证的蓝图
auth_bp = Blueprint('auth', __name__)


# 进行登录的视图函数
@auth_bp.route('/login')
def login():
    pass


# 退出登录
@auth_bp.route('/logout')
def logout():
    pass
