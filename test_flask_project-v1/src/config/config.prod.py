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
MAIL_SERVER = 'smtp.sina.cn'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'lzy11001@sina.cn'  # 你的邮箱
MAIL_PASSWORD = '4f42074fb975811a'  # 你的邮箱密码或应用专用密码
MAIL_DEFAULT_SENDER = 'lzy11001@sina.cn'  # 默认发件人

# 客户端上传文件的保存路径
SOURCE_ROOT = "D:\\Code\\test_project\\test_flask_project-v1\\source_root\\upload\\"