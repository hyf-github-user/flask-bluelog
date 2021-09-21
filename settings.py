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
    # debug设置
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    # 配置数据库连接
    # mysql + pymysql://user:password@hostip:port/数据名称
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hu15879093053@localhost:3306/bluelog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # True时会追踪对象修改并且发送信号,需要额外的内存
    # 文章每页的文章数
    BLUELOG_POST_PER_PAGE = 5
    # 分类每页的分类数
    BLUELOG_CATEGORY_PER_PAGE = 3
    # 每页的评论数
    BLUELOG_COMMENT_PER_PAGE = 3
    # 管理文章的分页数
    BLUELOG_MANAGE_POST_PER_PAGE = 6
    # 邮箱配置
    BLUELOG_EMAIL = '1348977728@qq.com'
    MAIL_DEBUG = True  # 开启debug，便于调试看信息
    MAIL_SUPPRESS_SEND = False  # 发送邮件，为True则不发送
    MAIL_SERVER = 'smtp.qq.com'  # 电子邮件服务器的主机名或IP地址
    MAIL_PORT = 465  # 电子邮件服务器的端口
    MAIL_USE_TLS = False  # 启用传输层安全协议
    MAIL_USE_SSL = True  # 启用安全套接层协议
    MAIL_USERNAME = '1348977728@qq.com'  # 邮件账户用户名
    MAIL_PASSWORD = ''  # 邮件账户的密码
    MAIL_DEFAULT_SENDER = '1348977728@qq.com'  # 填邮箱，默认发送者
    # 主题设置
    # ('theme name', 'display name')
    BLUELOG_THEMES = {'perfect_blue': 'Perfect Blue', 'black_swan': 'Black Swan'}
    BLUELOG_SLOW_QUERY_THRESHOLD = 1
    # 上传文件设置
    BLUELOG_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    if not os.path.exists(BLUELOG_UPLOAD_PATH):
        os.mkdir(BLUELOG_UPLOAD_PATH)
    BLUELOG_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
    # 富文本设置
    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_FILE_UPLOADER = 'admin.upload_image'


# 俩种配置
class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True


class ProductionConfig(BaseConfig):
    ENV = 'production'
    DEBUG = False
