# 作者：我只是代码的搬运工
# coding:utf-8


from flask import Blueprint, render_template, request, current_app, url_for, flash, redirect, abort, make_response

# 创建一个blog蓝图 (博客前台)
from flask_login import current_user

from bluelog.emails import send_new_reply_email, send_new_comment_email
from bluelog.forms import AdminCommentForm, CommentForm
from bluelog.models import Post, Category, Comment
from bluelog.utils import redirect_back
from exts import db

blog_bp = Blueprint('blog', __name__)


# 首页路由
@blog_bp.route('/')
def index():
    # # 分页
    page = request.args.get('page', 1, type=int)
    # 获取每页的文章数
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    # 创建分页对象,按照时间降序查询文章
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=per_page)
    # 获取当前分页对象的所有文章
    posts = pagination.items
    return render_template('blog/index.html', pagination=pagination, posts=posts)


# 关于我路由
@blog_bp.route('/about')
def about():
    # 这里还可以进行优化
    return render_template('blog/about.html')


# 分类路由
@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    # 根据id查询category,不存在返回404
    category = Category.query.get_or_404(category_id)
    # 获取当前的页数
    page = request.args.get('page', 1, type=int)
    # 获取每页的分类数
    per_page = current_app.config['BLUELOG_CATEGORY_PER_PAGE']
    # 分页对象
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('blog/category.html', category=category, pagination=pagination, posts=posts)


# 文章详情路由
@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    # 根据id查找文章
    post = Post.query.get_or_404(post_id)
    # 获取当前的页数
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    # 获取评论分页对象(查询被管理员收到的评论)
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.asc()).paginate(
        page, per_page)
    comments = pagination.items
    # 如果管理员登录了
    if current_user.is_authenticated:
        # 管理员评论
        form = AdminCommentForm()
        form.author.data = current_user.name
        form.email.data = current_app.config['BLUELOG_EMAIL']
        form.site.data = url_for('blog.index')
        from_admin = True  # 判断评论是否来自管理员
        reviewed = True  # 判断管理员是否收到
    else:
        # 非管理员评论
        form = CommentForm()
        from_admin = False
        reviewed = False
    # 表单数据验证
    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.data
        body = form.body.data
        comment = Comment(
            author=author, email=email, site=site, body=body,
            from_admin=from_admin, post=post, reviewed=reviewed)
        replied_id = request.args.get('reply')
        if replied_id:
            # 查找需要回复的评论
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
            send_new_reply_email(replied_comment)
        db.session.add(comment)
        db.session.commit()
        if current_user.is_authenticated:  # 如果是管理员发表评论
            flash('评论发表成功!', 'success')
        else:
            flash('感谢你的评论,您的评论将在管理员收到之后才会发表!', 'info')
            send_new_comment_email(post)  # 发送评论通知给管理员邮箱
        return redirect(url_for('blog.show_post', post_id=post_id))
    return render_template('blog/post.html', post=post, pagination=pagination, form=form, comments=comments)


# 回复评论,相对于一个中间站,把数据转发给show_post
@blog_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if not comment.post.can_comment:
        flash('评论已被禁止!', 'warning')
        return redirect(url_for('.show_post', post_id=comment.post.id))
    return redirect(
        url_for('.show_post', post_id=comment.post_id, reply=comment_id, author=comment.author) + '#comment-form')


# 切换主题的视图
@blog_bp.route('/change-theme/<theme_name>')
def change_theme(theme_name):
    if theme_name not in current_app.config['BLUELOG_THEMES'].keys():
        abort(404)

    response = make_response(redirect_back())
    response.set_cookie('theme', theme_name, max_age=30 * 24 * 60 * 60)
    return response
