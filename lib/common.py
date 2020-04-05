import hashlib
import logging.config

from conf import settings


# 密码加密
def convert_to_md5(data):
    data_salt = f'2020{data}2020'
    md5_obj = hashlib.md5()
    md5_obj.update(data_salt.encode('utf-8'))
    return md5_obj.hexdigest()


# 登录认证装饰器
def login_auth(func):
    from core import src

    def wrapper(*args, **kwargs):
        if src.user_logged is None:
            print('请登录。')
            src.login()
        return func(*args, **kwargs)
    return wrapper


# 获取日志对象
def get_logger(log_type):
    logging.config.dictConfig(settings.LOGGING_DIC)
    return logging.getLogger(log_type)
