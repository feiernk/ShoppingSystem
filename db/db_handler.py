import json
import os

from conf import settings


def read_data(filepath):
    with open(filepath, mode='rt', encoding='utf-8') as f:
        return json.load(f)


def write_data(filepath, data):
    with open(filepath, mode='wt', encoding='utf-8') as f:
        json.dump(data, f)


# 检查文件是否存在
def check_existed_user(un):
    user_filepath = os.path.join(settings.USER_DATA_FOLDER_PATH, f'{un}.json')
    return os.path.exists(user_filepath)


# 获取用户数据
def get_user_data(un):
    user_filepath = os.path.join(settings.USER_DATA_FOLDER_PATH, f'{un}.json')
    return read_data(user_filepath)


# 保存用户数据
def save_user_data(un, data):
    filepath = os.path.join(settings.USER_DATA_FOLDER_PATH, f'{un}.json')
    write_data(filepath, data)



