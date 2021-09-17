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
    send_mail(subject='评论通知消息', to=current_app.config['BLUELOG_EMAIL'],
              html='<p>在文章中有人提交了新的评论 <i>%s</i>, 点击了解详情</p>'
                   '<p><a href="%s">%s</a></P>'
                   '<p><small style="color: #868e96">由于是管理员通知邮件,不用回复!</small></p>'
                   % (post.title, post_url, post_url))


def send_new_reply_email(comment):
    post_url = url_for('blog.show_post', post_id=comment.post_id, _external=True) + '#comments'
    send_mail(subject='New reply', to=comment.email,
              html='<p>New reply for the comment you left in post <i>%s</i>, click the link below to check: </p>'
                   '<p><a href="%s">%s</a></p>'
                   '<p><small style="color: #868e96">Do not reply this email.</small></p>'
                   % (comment.post.title, post_url, post_url))
