'''
項目運行所需的靜態資源配置文件，僅用於開發人員編寫
'''
import os

WORK_DIRECTORY = os.path.abspath('..')

STATIC_FILE = '/static'

STATIC_DIRECTORY = WORK_DIRECTORY + STATIC_FILE


DEVELOPMENT_MODE = {
    'debug': True
}

PRODUCT_MODE = {
    'debug': False
}

