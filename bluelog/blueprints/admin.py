# 作者：我只是代码的搬运工
# coding:utf-8
from flask import Blueprint, render_template
from flask_login import login_required

admin_bp = Blueprint('admin', __name__)


# 管理员创建文章
@admin_bp.route('/post/new', methods=['GET', 'POST'])
@login_required  # 确保管理员已登录
def new_post():
    return "我是创建文章,正在开发中~~~"


# 管理员创建分类
@admin_bp.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    return "我是创建分类,正在开发中~~~"


# 管理员创建链接
@admin_bp.route('/link/new', methods=['GET', 'POST'])
@login_required
def new_link():
    return "我是创建友情链接,正在开发中~~~"


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


# 管理员管理分类
@admin_bp.route('/category/manage')
@login_required
def manage_category():
    return "我是管理分类的,正在开发中~~~"


# 管理员管理链接
@admin_bp.route('/link/manage')
@login_required
def manage_link():
    return "我是管理友情链接的,正在开发中~~~"


# 个人设置的视图
@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required  # 确保管理员已登录
def settings():
    return "我是设置页面,正在开发中!"


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
