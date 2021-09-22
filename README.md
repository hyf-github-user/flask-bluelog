# flask-bluelog(因学业繁忙开发比较慢)
#### 目标
写一个最好的博客系统

#### 相关配置
1. MySQL(得已知用户密码,还得创建bluelog数据库,在settings更改用户名与密码,需提前建好数据库)
2. mail设置: 在setting有参考
3. mysql创建数据库:CREATE DATABASE `数据库名称` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
4. Windows在使用flask init命令时可能会缺失一个库,使用pipenv install 下载即可
#### 快速使用
1. pipenv install --dev --python=3.7,pipenv下载相关依赖(需先下载pipenv第三方库来管理虚拟环境: pip install pipenv)
2. pipenv shell ,       进入pipenv虚拟环境shell
3. python app.py db init ,    初始化数据库
4. python app.py db migrate , 迁移数据库
5. python app.py db upgrade , 同步数据库
6. flask init , (设置管理员账号密码)   
7. python app.py runserver, 默认localhost:5000



