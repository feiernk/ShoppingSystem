from db import db_handler
from lib import common


admin_logger = common.get_logger('admin')
user_logger = common.get_logger('user')


# 检查用户是否已存在
def check_existed_user(un):
    return db_handler.check_existed_user(un)


# 注册功能
def register(un, pw):
    user_dict = {
        'user_name': un,
        'password': common.convert_to_md5(pw),
        'is_admin': False,
        'locked': False,
        'balance': 50000,
        'bank_details': [],
        'shopping_cart': {},
    }
    db_handler.save_user_data(un, user_dict)
    msg = f'新用户{un}注册成功。'
    user_logger.info(msg)
    return True, msg


# 登录功能
def login(un, pw):
    user_dict = db_handler.get_user_data(un)
    pw_md5 = common.convert_to_md5(pw)
    if user_dict['locked']:
        msg = f'用户{un}已被锁定，禁止登录，强制退出。'
        user_logger.warn(msg)
        return None, msg
    if pw_md5 == user_dict['password']:
        msg = f'用户{un}登陆成功。'
        user_logger.info(msg)
        return True, msg
    else:
        msg = f'用户{un}的密码错误。'
        user_logger.warn(msg)
        return False, msg


# 判断用户是否为管理员
def check_admin(un):
    user_dict = db_handler.get_user_data(un)

    if not user_dict['is_admin']:
        msg = f'警告，普通用户{un}尝试使用管理员功能，强制退出。'
        admin_logger.info(msg)
        return False, msg
    else:
        msg = f'管理员{un}开始使用管理员功能。'
        admin_logger.info(msg)
        return True, msg


# 冻结账户
def frozen_acc(admin_un, frozen_un):
    frozen_user_dict = db_handler.get_user_data(frozen_un)
    frozen_user_dict['locked'] = True
    db_handler.save_user_data(frozen_un, frozen_user_dict)
    msg = f'用户{frozen_un}已被管理员{admin_un}冻结'
    admin_logger.info(msg)
    return True, msg


# 添加账户(只有管理员账户可以添加管理员用户)
def add_acc(admin_un, un, pw, bal_int, is_admin):
    user_dict = {
        'user_name': un,
        'password': common.convert_to_md5(pw),
        'is_admin': is_admin,
        'locked': False,
        'balance': bal_int,
        'bank_details': [],
        'shopping_cart': {},
    }
    db_handler.save_user_data(un, user_dict)
    msg = f'管理员{admin_un}注册新用户{un}成功。'
    admin_logger.info(msg)
    return True, msg


# 修改额度
def verify_bal(admin_un, un, bal):
    user_dict = db_handler.get_user_data(un)
    user_dict['balance'] = bal
    db_handler.save_user_data(un, user_dict)
    msg = f'管理员{admin_un}将用户{un}的余额修改为{bal}。'
    admin_logger.info(msg)
    return True, msg
