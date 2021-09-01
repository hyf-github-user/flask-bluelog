# 作者：我只是代码的搬运工
# coding:utf-8
from flask import Blueprint, redirect, url_for, flash, render_template

# 创建一个用户认证的蓝图
from flask_login import current_user, login_user, login_required, logout_user

from bluelog.models import Admin
from bluelog.forms import LoginForm
from bluelog.utils import redirect_back

auth_bp = Blueprint('auth', __name__)


# 进行登录的视图函数
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # 判断当前用户是否登录
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    # 登录表单
    form = LoginForm()
    # 检验表单数据
    if form.validate_on_submit():
        #获取输入表单的数据
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        # 查询管理员
        admin = Admin.query.first()
        if admin:
            # 检查用户名密码正确性
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('欢迎回来!', 'info')
                # 返回主页的函数
                return redirect_back()
            flash('用户名或密码错误!', 'warning')
        else:
            flash('无此账号!', 'warning')
    return render_template('auth/login.html', form=form)


# 退出登录
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出登录成功!', 'info')
    # 返回主页的函数
    return redirect_back()
