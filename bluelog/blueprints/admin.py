# 作者：我只是代码的搬运工
# coding:utf-8
from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import login_required, current_user

from bluelog.forms import PostForm, SettingForm, CategoryForm, LinkForm
from bluelog.models import Post, Category, Link
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
    print(category_id)
    pass


# 管理员删除分类
@admin_bp.route('/category/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    print(category_id)
    pass


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
    return "我是管理友情链接的,正在开发中~~~"


# 管理文章的视图
@admin_bp.route('/post/manage')
@login_required
def manage_post():
    return "我是管理文章,正在开发中~~~"


# 管理员管理评论
@admin_bp.route('/comment/manage')
@login_required
def manage_comment():
    return "我是管理评论的,正在开发中~~~"


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
    form.name = current_user.name
    form.blog_title = current_user.blog_title
    form.blog_sub_title = current_user.blog_sub_title
    form.about = current_user.about
    return render_template('admin/settings.html', form=form)


# 管理员编辑文章
@admin_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    print(post_id)
    pass


# 管理员删除文章
@admin_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    print(post_id)
    pass


# 管理员发表评论
@admin_bp.route('/post/<int:post_id>/set-comment', methods=['POST'])
@login_required
def set_comment(post_id):
    print(post_id)
    pass


# 管理员通过评论
@admin_bp.route('/comment/<int:comment_id>/approve', methods=['POST'])
@login_required
def approve_comment(comment_id):
    print(comment_id)
    pass


# 管理员删除评论
@admin_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    print(comment_id)
    pass


# 管理员编辑链接
@admin_bp.route('/link/<int:link_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_link(link_id):
    print(link_id)
    pass


# 管理员删除链接
@admin_bp.route('/link/<int:link_id>/delete', methods=['POST'])
@login_required
def delete_link(link_id):
    print(link_id)
    pass


# 管理员上传文件
@admin_bp.route('/uploads/<path:filename>')
def get_image(filename):
    print(filename)
    pass


# 管理员上传
@admin_bp.route('/upload', methods=['POST'])
def upload_image():
    pass
