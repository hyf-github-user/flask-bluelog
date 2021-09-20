# flask-bluelog(因学业繁忙开发比较慢)
#### 目标
写一个最好的博客系统

#### 相关配置
MySQL(得已知用户密码,还得创建bluelog数据库)

#### 快速使用
1. pipenv install --dev --python=3.7   pipenv下载相关依赖
2. pipenv shell        进入pipenv虚拟环境shell
3. python app.py db init     初始化数据库
4. python app.py db migrate  迁移数据库
5. python app.py db upgrade  同步数据库
6. python app.py runserver 默认localhost:5000


