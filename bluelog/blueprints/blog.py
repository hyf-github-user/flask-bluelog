# 作者：我只是代码的搬运工
# coding:utf-8
from flask import Blueprint, render_template, request, current_app

# 创建一个blog蓝图 (博客前台)
from bluelog.models import Post

blog_bp = Blueprint('blog', __name__)


# 首页路由
@blog_bp.route('/')
def index():
    # 分页
    # 根据URL获取页数
    page = request.args.get('page', 1, type=int)
    # 获取每页的页数
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    # 创建一个分页对象
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    # 获取当前页数的记录列表
    posts = pagination.items
    return render_template('blog/index.html', pagination=pagination, posts=posts)


# 关于我路由
@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')


# 分类路由
@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    print(category_id)
    return render_template('blog/category.html')


# 文章详情路由
@blog_bp.route('/post/<int:post_id>')
def show_post(post_id):
    print(post_id)
    return render_template('blog/post.html')
