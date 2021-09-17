# 作者：我只是代码的搬运工
# coding:utf-8
import os

basedir = os.path.dirname(__file__)


# # 加一个平台检测
# WIN = sys.platform.startswith('win')
# if WIN:
#     prefix = 'sqlite:///'
# else:
#     prefix = 'sqlite:////'   # 一般针对Linux或Mac


class BaseConfig(object):
    # session加密
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')
    # 配置数据库连接
    # mysql + pymysql://user:password@hostip:port/databasename
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hu15879093053@localhost:3306/bluelog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # True时会追踪对象修改并且发送信号,需要额外的内存
    # 文章每页的文章数
    BLUELOG_POST_PER_PAGE = 5
    # 分类每页的分类数
    BLUELOG_CATEGORY_PER_PAGE = 3
    # 每页的评论数
    BLUELOG_COMMENT_PER_PAGE = 3
    # 邮箱
    BLUELOG_EMAIL = '1348977728@qq.com'
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    BLUELOG_EMAIL = os.getenv('BLUELOG_EMAIL')


# 俩种配置
class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True


class ProductionConfig(BaseConfig):
    ENV = 'production'
    DEBUG = False
