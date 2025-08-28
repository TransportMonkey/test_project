from flask_mail import Mail
import traceback
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED, FIRST_EXCEPTION
from contextlib import contextmanager
import threading
import flask
from flask import current_app
from functools import wraps
from common import logmode

def get_email()->Mail:
    return current_app.mail

def get_config(key:str, default_value=0):
    result = current_app.get_config(key, default_value)
    return result


def _my_find_app():
    return getattr(flask, "my_app", None)


def thread_session_wrapper(
        func,
        context_kwargs=None, env_kwargs=None):
    """ 自定义线程初始化,
    :param func 执行函数
    :param context_kwargs: dict, 上下文字典, 会初始化到request里面
    :param env_kwargs: dict, 环境字典
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        app = _my_find_app()
        envs = app.ctx_environs.copy()
        if env_kwargs:
            envs.update(env_kwargs)

        ctx = app.request_context(envs)
        # else:
        #     ctx = None

        try:
            # if ctx is not None:
            ctx.push()
            if context_kwargs:
                _request = ctx.request
                for k, v in context_kwargs.items():
                    setattr(_request, k, v)
            return func(*args, **kwargs)
        except:
            logmode.exception("thread_session_wrapper catch func(%s) error", func)
        finally:
            ctx.pop()

    return wrapper


def _thread_check_result(future):
    """ no result thread, check exceptions then raise """
    try:
        future.result()
    except:
        traceback.print_exc()


class MyThreadPool(ThreadPoolExecutor):
    _local = threading.local()

    @property
    def local_ctx(self) -> dict:
        return getattr(self._local, '_context_', None)

    @contextmanager
    def with_context(self, context: dict):
        _old_ = self.local_ctx
        self._local._context_ = context
        try:
            yield self
        finally:
            self._local._context_ = _old_

    def thread_pool_submit(self, action, *args,
                           _pool=None,
                           context_kwargs: dict = None,
                           env_kwargs: dict = None,
                           **kw):
        """ 不能用位置参数
        :param action: {function} 由线程执行的具体方法
        :param _pool: ThreadPoolExecutor, 线程池, None=使用默认的
        :param context_kwargs: dict, 上下文字典, 会初始化到request里面
        :param env_kwargs: dict, 环境字典
        """
        if context_kwargs is None:
            context_kwargs = {}
        action = thread_session_wrapper(
            action,
            context_kwargs=context_kwargs, env_kwargs=env_kwargs,
        )
        if _pool is None:
            _pool = self
        future = _pool.submit(action, *args, **kw)
        future.add_done_callback(_thread_check_result)
        return future

    @classmethod
    def thread_pool_wait(cls, futures, timeout=None, return_when=0):
        """ 等待多个线程任务完成,
        :param futures: list[Future] 任务对象列表
        :param timeout: int, 最大等待的超时时间(秒)
        :param return_when: int, 0=ALL_COMPLETED, 1=FIRST_COMPLETED 2=FIRST_EXCEPTION
            FIRST_COMPLETED = 'FIRST_COMPLETED'
            FIRST_EXCEPTION = 'FIRST_EXCEPTION'
            ALL_COMPLETED = 'ALL_COMPLETED'
        Returns:
            A named 2-tuple of sets. The first set, named 'done', contains the
            futures that completed (is finished or cancelled) before the wait
            completed. The second set, named 'not_done', contains uncompleted
            futures.
        """
        rw = ALL_COMPLETED
        if return_when == 1:
            rw = FIRST_COMPLETED
        elif return_when == 2:
            rw = FIRST_EXCEPTION
        return wait(futures, timeout=timeout, return_when=rw)


thread_pool = MyThreadPool(max_workers=200)
