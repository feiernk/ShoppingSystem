from db import db_handler
from conf import settings
from lib import common


shop_logger = common.get_logger('shop')


# 获取商品信息
def get_commodity_list():
    commodity_list = db_handler.read_data(settings.COMMODITY_DATA_FILEPATH)
    return commodity_list


# 保存购物车
def save_shopping_cart(un, shopping_cart_dict):
    user_dict = db_handler.get_user_data(un)
    user_shopping_cart_dict = user_dict['shopping_cart']
    for each_key, each_value in shopping_cart_dict.items():
        if each_key not in user_shopping_cart_dict:
            user_shopping_cart_dict[each_key] = each_value
        else:
            user_shopping_cart_dict[each_key]['count'] += each_value['count']
    user_dict['shopping_cart'] = user_shopping_cart_dict
    db_handler.save_user_data(un, user_dict)
    msg = f'用户{un}保存购物车成功。'
    shop_logger.info(msg)
    return True, msg


# 查看购物车功能
def get_shopping_cart_dict(un):
    user_dict = db_handler.get_user_data(un)
    msg = f'用户{un}查看购物车。'
    shop_logger.info(msg)
    return user_dict['shopping_cart']


# 清空购物车
def clear_shopping_cart(un):
    user_dict = db_handler.get_user_data(un)
    user_dict['shopping_cart'] = {}
    db_handler.save_user_data(un, user_dict)
    msg = f'用户{un}清空购物车。'
    shop_logger.info(msg)
    return True, msg

