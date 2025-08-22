# config.py


# 本地环境
ENV = "development"

# 调试信息
DEBUG = False

# 设置Token过期时间
EXPIRED_TIME = 48

# 数据库配置
# SQLALCHEMY_DATABASE_URI = f'sqlite:///../{os.path.join("db", "test.db")}'
SQLALCHEMY_DATABASE_URI = f'mysql://root:lzy110101@localhost:3306/prod'

# 邮箱配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = '792728404@qq.com'  # 你的邮箱
MAIL_PASSWORD = 'fayirmgekhgibcef'  # 你的邮箱密码或应用专用密码
MAIL_DEFAULT_SENDER = '792728404@qq.com'  # 默认发件人

# 客户端上传文件的保存路径
SOURCE_ROOT = "D:\\Code\\test_project\\test_flask_project-v1\\source_root\\upload\\"