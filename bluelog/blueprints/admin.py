# 作者：我只是代码的搬运工
# coding:utf-8
import os

from flask import Blueprint, flash, render_template, redirect, url_for, request, current_app, send_from_directory
from flask_ckeditor import upload_fail, upload_success
from flask_login import login_required, current_user

from bluelog.forms import PostForm, SettingForm, CategoryForm, LinkForm
from bluelog.models import Post, Category, Link, Comment
from bluelog.utils import redirect_back, allowed_file
from exts import db

admin_bp = Blueprint('admin', __name__)


# 管理员创建文章
@admin_bp.route('/post/new', methods=['GET', 'POST'])
@login_required  # 确保管理员已登录
def new_post():
    # 创建文章表单
    form = PostForm()
    # 数据验证
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        post = Post(title=title, body=body, category=category)
        # 开始提交到数据库
        db.session.add(post)
        db.session.commit()
        # flash提示信息
        flash("文章已创建!", 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    # 使用富文本
    return render_template('admin/new_post.html', form=form)


# 管理文章的视图
@admin_bp.route('/post/manage')
@login_required
def manage_post():
    # 对所有文章进行分类
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config[
        'BLUELOG_MANAGE_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('admin/manage_post.html', pagination=pagination, posts=posts, page=page)


# 管理员编辑文章
@admin_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category = Category.query.get(form.category.data)
        db.session.commit()
        flash("文章更新成功!", 'success')
        return redirect(url_for('blog.show_post'))
    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_id
    return render_template('admin/edit_post.html', form=form)


# 管理员删除文章
@admin_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('.manage_post'))


# 管理员创建分类
@admin_bp.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    # 创建表单
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        # 创建新的分类
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('分类创建成功!', 'success')
        return redirect(url_for('.manage_category'))
    return render_template('admin/new_category.html', form=form)


# 管理员管理分类
@admin_bp.route('/category/manage')
@login_required
def manage_category():
    return render_template('admin/manage_category.html')


# 管理员编辑分类
@admin_bp.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    # 编辑的表单
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)
    if category_id == 1:
        flash("默认分类无法修改!", 'warning')
        return redirect(url_for('.manage_category'))
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash("分类数据更新成功!", "success")
        return redirect(url_for('.manage_category'))
    form.name.data = category.name
    return render_template('admin/edit_category.html', form=form)


# 管理员删除分类
@admin_bp.route('/category/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('./manage_category'))


# 管理员创建链接
@admin_bp.route('/link/new', methods=['GET', 'POST'])
@login_required
def new_link():
    form = LinkForm()
    if form.validate_on_submit():
        name = form.name.data
        url = form.url.data
        link = Link(name=name, url=url)
        db.session.add(link)
        db.session.commit()
        flash("友情链接创建成功!", "success")
        return redirect(url_for('.manage_link'))
    return render_template('admin/new_link.html', form=form)


# 管理员管理链接
@admin_bp.route('/link/manage')
@login_required
def manage_link():
    return render_template('admin/manage_link.html')


# 管理员编辑链接
@admin_bp.route('/link/<int:link_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_link(link_id):
    form = LinkForm()
    link = Link.query.get_or_404(link_id)
    if form.validate_on_submit():
        link.name = form.name.data
        link.url = form.url.data
        db.session.commit()
        flash('友情链接更新成功!', 'success')
        return redirect(url_for('.manage_link'))
    form.name.data = link.name
    form.url.data = link.url
    return render_template('admin/edit_link.html', form=form)


# 管理员删除链接
@admin_bp.route('/link/<int:link_id>/delete', methods=['POST'])
@login_required
def delete_link(link_id):
    link = Link.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    flash('友情链接删除成功!', 'success')
    return redirect(url_for('.manage_link'))


# 管理员发表评论
@admin_bp.route('/post/<int:post_id>/set-comment', methods=['POST'])
@login_required
def set_comment(post_id):
    post = Post.query.get_or_404(post_id)
    # 查询是否能发布评论
    if post.can_comment:
        post.can_comment = False
        flash("评论功能已禁止!", 'success')
    else:
        post.can_comment = True
        flash('评论功能已启动!', 'success')
    # 更新数据库
    db.session.commit()
    return redirect_back()


# 管理员管理评论
@admin_bp.route('/comment/manage')
@login_required
def manage_comment():
    filter_rule = request.args.get('filter', 'all')  # 第一级评论筛选条件
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    if filter_rule == 'unread':
        filtered_comments = Comment.query.filter_by(reviewed=False)
    elif filter_rule == 'admin':
        filtered_comments = Comment.query.filter_by(from_admin=True)
    else:
        filtered_comments = Comment.query    # all的情况

    pagination = filtered_comments.order_by(Comment.timestamp.desc()).paginate(page, per_page=per_page)
    comments = pagination.items
    return render_template('admin/manage_comment.html', comments=comments, pagination=pagination)


# 管理员通过评论
@admin_bp.route('/comment/<int:comment_id>/approve', methods=['POST'])
@login_required
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.reviewed = True
    db.session.commit()
    flash('评论已批准发布!', 'success')
    return redirect_back()


# 管理员删除评论
@admin_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('.manage_comment'))


# 个人设置的视图
@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required  # 确保管理员已登录
def settings():
    # 设置表单
    form = SettingForm()
    # 数据验证
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.blog_title = form.blog_title.data
        current_user.blog_sub_title = form.blog_sub_title.data
        current_user.about = form.about.data
        db.session.commit()
        flash('设置更新成功!', 'success')
        return redirect(url_for('blog.index'))
    # 展示之前填充的数据
    form.name.data = current_user.name
    form.blog_title.data = current_user.blog_title
    form.blog_sub_title.data = current_user.blog_sub_title
    form.about.data = current_user.about
    return render_template('admin/settings.html', form=form)


# 管理员上传文件
@admin_bp.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(current_app.config['BLUELOG_UPLOAD_PATH'], filename)


# 管理员上传
@admin_bp.route('/upload', methods=['POST'])
def upload_image():
    f = request.files.get('upload')
    if not allowed_file(f.filename):
        return upload_fail('必须是照片!')
    f.save(os.path.join(current_app.config['BLUELOG_UPLOAD_PATH'], f.filename))
    url = url_for('.get_image', filename=f.filename)
    return upload_success(url, f.filename)
