# 作者：我只是代码的搬运工
# coding:utf-8

# 管理员模型
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from exts import db


# 博客用户模型
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))  # 管理员的名称
    password_hash = db.Column(db.String(128))  # 密码的哈希值
    blog_title = db.Column(db.String(60))  # 博客标题
    blog_sub_title = db.Column(db.String(100))  # 博客的副标题
    name = db.Column(db.String(30))  # 管理员名字
    about = db.Column(db.Text)  # 管理员简介

    # 设置密码与验证密码
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


# 分类模型
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)  # 分类的名称
    posts = db.relationship('Post', back_populates='category')  # 分类与文章一对多的关系


# 文章模型
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # 定义模型之间的关系
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')
    # 文章与评论是一对多关系
    comments = db.relationship('Comment', back_populates='post', cascade='all,delete-orphan')


# 评论模型
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)  # 判断是否是管理员的评论
    reviewed = db.Column(db.Boolean, default=False)  # 判断是否通过审核
    # 自身id为外键(也叫邻接列表关系)
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    # remote_side对应多个回复对应一个评论
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
    # cascade='all',当父评论删除之后,所有的子评论全部删除
    replies = db.relationship('Comment', back_populates='replied', cascade='all')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    # 文章与评论是一对多关系
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    url = db.Column(db.String(255))
