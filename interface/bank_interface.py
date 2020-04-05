from db import db_handler
from lib import common


bank_logger = common.get_logger('bank')


# 查看余额
def check_bal(un):
    user_dict = db_handler.get_user_data(un)
    bal = user_dict['balance']
    msg = f'用户{un}的余额为{bal}'
    bank_logger.info(msg)
    return True, msg


# 提现
def get_cash(un, cash):
    user_dict = db_handler.get_user_data(un)
    bal_float = float(user_dict['balance'])
    cash_float = float(cash)
    fee_float = cash_float * 0.05  # 手续费
    total_float = cash_float + fee_float  # 总额
    if bal_float < total_float:
        msg = f'用户{un}余额不足，手续费为{fee_float}，余额为{bal_float}，提现失败。'
        bank_logger.warn(msg)
        return False, msg
    else:
        bal_float -= total_float
        user_dict['balance'] = bal_float
        db_handler.save_user_data(un, user_dict)
        msg = f'用户{un}提取金额{cash_float}，手续费为{fee_float}，余额为{bal_float}，提现成功。'
        bank_logger.info(msg)
        add_bank_details(un, msg)
        return True, msg


# 还款
def repay(un, cash):
    user_dict = db_handler.get_user_data(un)
    bal_float = float(user_dict['balance'])
    cash_float = float(cash)
    bal_float += cash_float
    user_dict['balance'] = bal_float
    db_handler.save_user_data(un, user_dict)
    msg = f'用户{un}还款金额{cash_float}，余额为{bal_float}，还款成功。'
    bank_logger.info(msg)
    add_bank_details(un, msg)
    return True, msg


# 转账
def transfer(un, target_un, cash):
    user_dict = db_handler.get_user_data(un)
    bal_float = float(user_dict['balance'])
    cash_float = float(cash)
    if bal_float < cash_float:
        msg = f'用户{un}余额不足，余额为{bal_float}，转账失败。'
        bank_logger.warn(msg)
        return False, msg
    else:
        bal_float -= cash_float
        user_dict['balance'] = bal_float
        db_handler.save_user_data(un, user_dict)

        target_user_dict = db_handler.get_user_data(target_un)
        target_user_dict['balance'] += cash_float
        db_handler.save_user_data(target_un, target_user_dict)
        msg = f'用户{un}向用户{target_un}转账金额{cash_float}，余额为{bal_float}，转账成功。'
        bank_logger.info(msg)
        add_bank_details(un, msg)
        return True, msg


# 添加流水
def add_bank_details(un, msg):
    user_dict = db_handler.get_user_data(un)
    user_dict['bank_details'].append(msg)
    db_handler.save_user_data(un, user_dict)


# 查看流水
def check_bank_details(un):
    user_dict = db_handler.get_user_data(un)
    detail_list = user_dict['bank_details']
    if not detail_list:
        msg = f'用户{un}没有银行流水信息。'
        bank_logger.info(msg)
        return False, msg, []
    else:
        msg = f'用户查看银行流水。'
        bank_logger.info(msg)
        return True, msg, detail_list


# 结账
def checkout(un):
    user_dict = db_handler.get_user_data(un)
    bal = user_dict['balance']
    shopping_cart_dict = user_dict['shopping_cart']
    total_cost = 0
    for each_value in shopping_cart_dict.values():
        total_cost += each_value['count'] * each_value['price']
    if bal < total_cost:
        msg = f'用户{un}余额不足，总共消费{total_cost}，余额为{bal}，结账失败。'
        bank_logger.warn(msg)
        return False, msg
    else:
        bal -= total_cost
        user_dict['balance'] = bal
        user_dict['shopping_cart'] = {}
        db_handler.save_user_data(un, user_dict)
        msg = f'用户{un}总共消费{total_cost}，余额为{bal}，结账成功。'
        bank_logger.info(msg)
        add_bank_details(un, msg)
        return True, msg

