from interface import user_interface
from interface import bank_interface
from interface import shop_interface
from lib import common

user_logged = None


# 注册
def register():
    while True:
        un_input = input('请输入用户名：').strip()
        if un_input == '':
            print('用户名不能为空。')
        elif user_interface.check_existed_user(un_input):
            print('用户名已存在。')
        else:
            break
    while True:
        pw_input = input('请输入密码：').strip()
        pw_re_input = input('请再次输入密码：').strip()
        if pw_input != pw_re_input:
            print('两次输入的密码不一致，请重新输入。')
        elif pw_input == '':
            print('密码不能为空。')
        else:
            break
    res_tuple = user_interface.register(un_input, pw_input)
    print(res_tuple[1])


# 登录
def login():
    while True:
        un_input = input('请输入用户名：').strip()
        if un_input == '':
            print('用户名不能为空。')
        elif not user_interface.check_existed_user(un_input):
            print('用户名不存在。')
        else:
            break
    while True:
        pw_input = input('请输入密码：').strip()
        res_tuple = user_interface.login(un_input, pw_input)
        if res_tuple[0] is None:
            print(res_tuple[1])
            quit()
        elif not res_tuple[0]:
            print(res_tuple[1])
            print('请重新输入密码。')
        else:
            global user_logged
            user_logged = un_input
            print(res_tuple[1])
            break


# 查看余额
@common.login_auth
def check_bal():
    res_tuple = bank_interface.check_bal(user_logged)
    print(res_tuple[1])


# 提现
@common.login_auth
def get_cash():
    print('使用提现功能需要收取5%的手续费。')
    while True:
        cash_input = input('请输入提现金额：').strip()
        if not cash_input.isdigit():
            print('金额只接受整数。')
        elif int(cash_input) == 0:
            print('金额不能为0。')
        else:
            break
    res_tuple = bank_interface.get_cash(user_logged, cash_input)
    print(res_tuple[1])


# 还款
@common.login_auth
def repay():
    while True:
        cash_input = input('请输入还款金额：').strip()
        if not cash_input.isdigit():
            print('金额只接受整数。')
        elif int(cash_input) == 0:
            print('金额不能为0。')
        else:
            break
    res_tuple = bank_interface.repay(user_logged, cash_input)
    print(res_tuple[1])


# 转账
@common.login_auth
def transfer():
    while True:
        un_input = input('请输入目标用户名：').strip()
        if un_input == '':
            print('用户名不能为空。')
        elif not user_interface.check_existed_user(un_input):
            print('用户名不存在。')
        elif un_input == user_logged:
            print('目标用户不能为登录用户。')
        else:
            break
    while True:
        cash_input = input('请输入转账金额：').strip()
        if not cash_input.isdigit():
            print('金额只接受整数。')
        elif int(cash_input) == 0:
            print('金额不能为0。')
        else:
            break
    res_tuple = bank_interface.transfer(user_logged, un_input, cash_input)
    print(res_tuple[1])


# 查看流水
@common.login_auth
def check_bank_details():
    res_tuple = bank_interface.check_bank_details(user_logged)
    if not res_tuple[0]:
        print(res_tuple[1])
    else:
        detail_list = res_tuple[2]
        for each_detail in detail_list:
            print(each_detail)


# 购物功能1 添加购物车
@common.login_auth
def add_shopping_cart():
    shopping_cart_dict = {}
    commodity_list = shop_interface.get_commodity_list()
    while True:
        while True:
            show_all_commodity(commodity_list)
            num_input = input('请输入商品编号：').strip()
            num_int = int(num_input)
            if num_int not in range(len(commodity_list)):
                print('只接受商品编号，请重新输入。')
            else:
                selected_commodity_dict = commodity_list[num_int]
                break
        while True:
            cnt_input = input('请输入购买数量：').strip()
            if not cnt_input.isdigit():
                print('只接受数字。')
            elif int(cnt_input) == 0:
                print('购买数量不能为0。')
            else:
                cnt_int = int(cnt_input)
                selected_commodity_name = selected_commodity_dict['name']
                selected_commodity_price = selected_commodity_dict['price']
                if selected_commodity_name not in shopping_cart_dict:
                    shopping_cart_dict[selected_commodity_name] = {'price': selected_commodity_price, 'count': cnt_int}
                else:
                    shopping_cart_dict[selected_commodity_name]['count'] += cnt_int
                break
        while True:
            confirm_input = input('请输入下一步操作，y: 继续购物车，n：保存购物车并退出，quit：不保存购物车并退出。')
            if confirm_input.lower() == 'y':
                break
            elif confirm_input.lower() == 'n':
                print('请去[查看购物车]中进行结算。')
                res_tuple = shop_interface.save_shopping_cart(user_logged, shopping_cart_dict)
                print(res_tuple[1])
                return
            elif confirm_input.lower() == 'quit':
                return
            else:
                print('非法输入，只接受 y/Y，n/N，quit')


# 打印商品信息
def show_all_commodity(commodity_list):
    print('\n')
    for num, each_dict in enumerate(commodity_list):
        name = each_dict['name']
        price = each_dict['price']
        print(f'商品编号：{num}，商品名称：{name}，价格：{price}')
    print('\n')


# 购物功能2 查看购物车功能，结算功能
@common.login_auth
def check_shopping_cart():
    shopping_cart_dict = shop_interface.get_shopping_cart_dict(user_logged)
    if not shopping_cart_dict:
        print('购物车为空。')
    else:
        for each_key, each_dict in shopping_cart_dict.items():
            print(f'商品名称：{each_key}，商品价格：{each_dict["price"]}，商品数量：{each_dict["count"]}')
        while True:
            confirm_input = input('请输入下一步操作，y: 结算，n：退出，clear：清空购物车。')
            if confirm_input.lower() == 'y':
                res_tuple = bank_interface.checkout(user_logged)
                print(res_tuple[1])
                return
            elif confirm_input.lower() == 'n':
                return
            elif confirm_input.lower() == 'clear':
                res_tuple = shop_interface.clear_shopping_cart(user_logged)
                print(res_tuple[1])
                return
            else:
                print('非法输入，只接受 y/Y，n/N，clear')


# 管理员功能
@common.login_auth
def admin_manage():
    res_tuple = user_interface.check_admin(user_logged)
    if not res_tuple[0]:
        print(res_tuple[1])
        exit()
    else:
        print(res_tuple[1])

    # 冻结账户
    def frozen_acc():
        while True:
            un_input = input('请输入冻结用户的用户名：').strip()
            if un_input == '':
                print('用户名不能为空。')
            elif not user_interface.check_existed_user(un_input):
                print('用户名不存在。')
            else:
                break
        res_tuple = user_interface.frozen_acc(user_logged, un_input)
        print(res_tuple[1])

    # 添加账户(只有管理员账户可以添加管理员用户)
    def add_acc():
        while True:
            un_input = input('请输入用户名：').strip()
            if un_input == '':
                print('用户名不能为空。')
            elif user_interface.check_existed_user(un_input):
                print('用户名已存在。')
            else:
                break
        while True:
            pw_input = input('请输入密码：').strip()
            pw_re_input = input('请再次输入密码：').strip()
            if pw_input != pw_re_input:
                print('两次输入的密码不一致，请重新输入。')
            elif pw_input == '':
                print('密码不能为空。')
            else:
                break
        while True:
            bal_input = input('请输入账户初始余额：').strip()
            if not bal_input.isdigit():
                print('只接受数字。')
            else:
                bal_int = int(bal_input)
                break
        while True:
            is_admin_input = input('是否为管理员用户？y/n').strip()
            if is_admin_input.lower() == 'y':
                is_admin = True
                break
            elif is_admin_input.lower() == 'n':
                is_admin = False
                break
            else:
                print('非法输入，只接受y/Y, n/N。')
        res_tuple = user_interface.add_acc(user_logged, un_input, pw_input, bal_int, is_admin)
        print(res_tuple[1])

    # 修改额度
    def verify_bal():
        while True:
            un_input = input('请输入用户名：').strip()
            if un_input == '':
                print('用户名不能为空。')
            elif not user_interface.check_existed_user(un_input):
                print('用户名不存在。')
            else:
                break
        while True:
            bal_input = input('请输入账户余额：').strip()
            if not bal_input.isdigit():
                print('只接受数字。')
            else:
                bal_int = int(bal_input)
                break
        res_tuple = user_interface.verify_bal(user_logged, un_input, bal_int)
        print(res_tuple[1])

    cmd_dict = {
        '0': ('退出', exit),
        '1': ('冻结账户', frozen_acc),
        '2': ('添加账户', add_acc),
        '3': ('修改额度', verify_bal),
    }
    cmd_info = ''
    for each_num, each_tuple in cmd_dict.items():
        cmd_info += f'管理员功能编号：{each_num}，管理员功能名称：{each_tuple[0]}\n'
    while True:
        print('\n')
        print(cmd_info)
        print('\n')
        cmd_input = input('请输入功能编号：').strip()
        if cmd_input not in cmd_dict:
            print('只接受提示信息中存在的功能编号。')
        else:
            # 执行功能
            cmd_dict[cmd_input][1]()


def run():
    print('开始运行主程序。')
    cmd_dict = {
        '0': ('退出', exit),
        '1': ('注册', register),
        '2': ('登录', login),
        '3': ('查看余额', check_bal),
        '4': ('提现', get_cash),
        '5': ('还款', repay),
        '6': ('转账', transfer),
        '7': ('查看流水', check_bank_details),
        '8': ('添加购物车', add_shopping_cart),
        '9': ('查看购物车(包括结算功能)', check_shopping_cart),
        '10': ('管理员功能', admin_manage),
    }
    cmd_info = ''
    for each_num, each_tuple in cmd_dict.items():
        cmd_info += f'功能编号：{each_num}，功能名称：{each_tuple[0]}\n'
    while True:
        print('\n')
        print(cmd_info)
        print('\n')
        cmd_input = input('请输入功能编号：').strip()
        if cmd_input not in cmd_dict:
            print('只接受提示信息中存在的功能编号。')
        else:
            # 执行功能
            cmd_dict[cmd_input][1]()
