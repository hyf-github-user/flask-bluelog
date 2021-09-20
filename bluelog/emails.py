# 作者：我只是代码的搬运工
# coding:utf-8
from threading import Thread

from flask import url_for, current_app
from flask_mail import Message

from exts import mail


# 发送邮件
def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_mail(subject, to, html):
    app = current_app._get_current_object()
    message = Message(subject, recipients=[to], html=html)
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


def send_new_comment_email(post):
    post_url = url_for('blog.show_post', post_id=post.id, _external=True) + '#comments'
    send_mail(subject='评论通知消息', to=current_app.config['MAIL_DEFAULT_SENDER'],
              html='<p>在文章中有人提交了新的评论,发送者的邮箱地址请登录管理后台查看! <hr>'
                   '标题为:<i>%s</i>的文章, 点击了解详情</p>'
                   '<p><a href="%s">%s</a></P>'
                   '<p><small style="color: #868e96">由于是管理员通知邮件,不用回复!</small></p>'
                   % (post.title, post_url, post_url))


def send_new_reply_email(comment):
    post_url = url_for('blog.show_post', post_id=comment.post_id, _external=True) + '#comments'
    send_mail(subject='新的回复', to=comment.email,
              html='<p>有针对文章的新回复发布了,<hr>'
                   '该文章的标题是: <i>%s</i>的文章, 点击了解详情</p>'
                   '<p><a href="%s">%s</a></p>'
                   '<p><small style="color: #868e96">由于是管理员通知邮件,不用回复!</small></p>'
                   % (comment.post.title, post_url, post_url))



