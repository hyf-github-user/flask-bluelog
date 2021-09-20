# 作者：我只是代码的搬运工
# coding:utf-8
import click
from flask import Flask, render_template
from flask_login import current_user
from flask_wtf.csrf import CSRFError

from bluelog.blueprints.admin import admin_bp
from bluelog.blueprints.auth import auth_bp
from bluelog.blueprints.blog import blog_bp
from bluelog.models import Admin, Category, Link, Comment
from exts import db, bootstrap, mail, ckeditor, moment, login_manager, toolbar, csrf
from settings import DevelopmentConfig


def create_app():
    app = Flask('bluelog')
    app.config.from_object(DevelopmentConfig)
    # 初始化扩展
    register_extensions(app=app)
    # 注册蓝图
    register_blueprints(app=app)
    # 数据库数据初始化
    register_template_context(app=app)
    # 注册命令
    register_commands(app=app)
    # 定义错误页面
    register_errors(app=app)
    # 富文本编辑器配置
    # app.config['CKEDITOR_SERVE_LOCAL'] = True
    # app.config['CKEDITOR_FILE_UPLOADER'] = 'admin.upload_for_ckeditor'
    # app.config['MAIL_DEFAULT_SENDER'] = '1348977728@qq.com'  # 填邮箱，默认发送者
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
    # 初始化flask-login
    login_manager.init_app(app=app)
    # 初始化debug
    toolbar.init_app(app=app)
    # csrf验证
    csrf.init_app(app=app)


# 注册蓝图
def register_blueprints(app):
    # 注册蓝图
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')


# 定义错误页面
def register_errors(app):
    # 设置404页面
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    # 设置500页面
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/404.html', description=e.description), 400


# 定义模板上下文处理函数
def register_template_context(app):
    @app.context_processor
    def make_template_context():
        # 查找admin与categories
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        links = Link.query.order_by(Link.name).all()
        # unread_comments存储没被审核的评论
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(admin=admin, categories=categories, links=links, unread_comments=unread_comments)


# 生成命令
def register_commands(app):
    # 初始化数据库命令
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('这个操作将会删除数据库的数据,你确定继续这个操作吗?', abort=True)
            db.drop_all()
            click.echo('删除数据库')
        db.create_all()
        click.echo('初始化数据库')

    # 初始化蓝客设置管理员密码的命令
    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
        """Building Bluelog, just for you."""

        click.echo('初始化数据库中.....')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            click.echo('管理员账户已存在,正在更新管理员信息....')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('创建管理员账户中.....')
            admin = Admin(
                username=username,
                blog_title='蓝客',
                blog_sub_title="我是副标题",
                name='hyf',
                about='我是简介呀!'
            )
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo('创建默认分类中....')
            category = Category(name='默认')
            db.session.add(category)

        db.session.commit()
        click.echo('完成!')

    # 生成虚拟数据命令
    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
    def forge(category, post, comment):
        """Generate fake data."""
        from bluelog.fakes import fake_admin, fake_categories, fake_posts, fake_comments, fake_links

        db.drop_all()
        db.create_all()

        click.echo('创建 %d 个分类中...' % category)
        fake_categories(category)

        click.echo('创建 %d 篇文章...' % post)
        fake_posts(post)

        click.echo('创建 %d 个评论...' % comment)
        fake_comments(comment)

        click.echo('创建链接中...')
        fake_links()

        click.echo('完成!')
