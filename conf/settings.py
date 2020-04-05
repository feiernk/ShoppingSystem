import os
import sys


BASE_PATH = os.path.dirname(os.path.dirname(__file__))

DB_PATH = os.path.join(BASE_PATH, 'db')

USER_DATA_FOLDER_PATH = os.path.join(DB_PATH, 'user_data')

COMMODITY_DATA_FILEPATH = os.path.join(DB_PATH, 'commodity_data', 'commodity_data.json')

LOG_FOLDER_PATH = os.path.join(BASE_PATH, 'log')

LOG_FILEPATH = os.path.join(LOG_FOLDER_PATH, 'shop_atm.log')


# 日志格式
standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]'

# 日志配置字典
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard_format': {
            'format': standard_format
        },
    },
    'handlers': {
        'standard_handler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'standard_format',
            'filename': LOG_FILEPATH,
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        '': {
            'handlers': ['standard_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}