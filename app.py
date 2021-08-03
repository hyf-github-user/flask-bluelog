from flask import render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from bluelog import create_app
from exts import db

app = create_app()  # 创建一个app对象

# 使用flask-script扩展对app进行绑定
manager = Manager(app=app)  # flask-script命令

# 数据库命令的配置
migrate = Migrate(app=app, db=db)
# 把命令添加到flask-script命令,MigrateCommand这个只有flask_migrate版本是2.5.3才具有的 此时的flask的版本必须是1.1.2
manager.add_command('db', MigrateCommand)


@app.route('/')
def index():
    return render_template('errors/404.html')


# 设置404页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html')


# 设置500页面
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html')


if __name__ == '__main__':
    manager.run()
