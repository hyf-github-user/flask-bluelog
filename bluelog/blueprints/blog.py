# 作者：我只是代码的搬运工
# coding:utf-8
from flask import Blueprint, render_template

# 创建一个blog蓝图 (博客前台)
from bluelog.models import Post

blog_bp = Blueprint('blog', __name__)


# 首页路由
@blog_bp.route('/')
def index():
    # 查询所有的文章(安装时间降序排列)
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('blog/index.html', posts=posts)


# 关于我路由
@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')


# 分类路由
@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    return render_template('blog/category.html')


# 文章详情路由
@blog_bp.route('/post/<int:post_id>')
def show_post(post_id):
    return render_template('blog/post.html')
