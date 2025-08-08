import os
from common import logmode, db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix
import pymysql

class MyApp(Flask):
    NAME = 'test_flask'
    SHORT_NAME = "test"
    LOG_PATH = "logs"

    inited = False
    root: Api
    db: SQLAlchemy

    def __init__(self):
        super(MyApp, self).__init__(__name__)
        self.wsgi_app = ProxyFix(self.wsgi_app)
        self.init_app()

    def init_app(self):
        if self.inited:
            return
        self._init_config()
        self._init_log()
        self._init_redis()

        self._init_sqlalchemy()
        self.init_route()
        self.inited = True

    def get_config(self, name: str, default=None):
        """获取配置，环境变量优先，没有才从配置读取
        :param name: 配置名，忽略大小写，全部转换成大写
        :param default: 默认值，当读不到配置时，返回的值
        """
        name = name.upper()
        env_value = os.environ.get(name)
        if env_value is not None:
            return env_value
        return self.config.get(name, default)

    def _init_config(self):
        env = os.environ.get('CONFIG_ENV', "dev").lower()  # dev, pre, prod
        config_file = f"config.{env}.py"
        file_path = os.path.join(self.root_path, "config", config_file) # 拼接config_file完整的路径
        self.config.from_pyfile(file_path) # 用于从一个 Python 文件中加载配置。

    def _init_log(self):
        log_path = os.environ.get("LOG_PATH", self.LOG_PATH)
        if log_path:
            log_path = os.path.abspath(log_path) # 获取log_path绝对路径
            logmode.log_init(log_path, self.config["DEBUG"])

    def _init_redis(self):
        pass

    def _init_sqlalchemy(self):
        pymysql.install_as_MySQLdb()
        db.db = SQLAlchemy(app=self, model_class=db.BaseModel)
        with self.app_context():
            db.BaseModel.set_session(db.db.session)
        self.db = db.db

        # self.teardown_appcontext_funcs.pop()  # remove flask_sqlalchemy's shutdown_session
        #
        # @self.teardown_appcontext
        # def shutdown_session(resp_or_exc):
        #     if db.db is None:
        #         return
        #     session = db.db.session
        #     commit = resp_or_exc is None
        #     try:
        #         if commit:
        #             session.commit()
        #     except:
        #         session.rollback()
        #         raise
        #     finally:
        #         session.remove()
        #     return resp_or_exc

    def init_route(self):
        root = Api(self)
        self.root = root

        from services import user,todo,blog
        for view in [user,todo,blog]:
            root.add_namespace(view.api) # user、todo模型获取api

    def run(self, **kwargs):
        super(MyApp, self).run(**kwargs)


if __name__ == "__main__":
    app = MyApp()
    app.run()
