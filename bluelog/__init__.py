# 作者：我只是代码的搬运工
# coding:utf-8
import click
from flask import Flask

from bluelog.blueprints.admin import admin_bp
from bluelog.blueprints.auth import auth_bp
from bluelog.blueprints.blog import blog_bp
from bluelog.models import Admin, Category
from exts import db, bootstrap, mail, ckeditor, moment, login_manager
from settings import DevelopmentConfig


def create_app():
    app = Flask('bluelog', template_folder='../templates', static_folder='../static')
    app.config.from_object(DevelopmentConfig)
    # 初始化扩展
    register_extensions(app=app)
    # 注册蓝图
    register_blueprints(app=app)
    # 数据库数据初始化
    register_template_context(app=app)
    # 注册命令
    register_commands(app=app)
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
    login_manager.init_app(app)


# 注册蓝图
def register_blueprints(app):
    # 注册蓝图
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')


# 定义模板上下文处理函数
def register_template_context(app):
    @app.context_processor
    def make_template_context():
        # 查找admin与categories
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        return dict(admin=admin, categories=categories)


# 生成命令
def register_commands(app):
    # 初始化数据库命令
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('初始化数据库')

    # 初始化蓝客设置管理员密码的命令
    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
        """Building Bluelog, just for you."""

        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating the temporary administrator account...')
            admin = Admin(
                username=username,
                blog_title='Bluelog',
                blog_sub_title="No, I'm the real thing.",
                name='Admin',
                about='Anything about you.'
            )
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo('Creating the default category...')
            category = Category(name='Default')
            db.session.add(category)

        db.session.commit()
        click.echo('Done.')

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

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d categories...' % category)
        fake_categories(category)

        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        click.echo('Generating %d comments...' % comment)
        fake_comments(comment)

        click.echo('Generating links...')
        fake_links()

        click.echo('Done.')
