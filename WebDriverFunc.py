from selenium import webdriver
from selenium.webdriver.common.by import By
import traceback
import time


def open_Chrome(user_data_path=r'C:\Users\wang\AppData\Local\Google\Chrome\User Data',
                implicit_waiting_time=5,
                is_self_closing=True):
    """
    :param user_data_path: Chrome的用户信息路径
    :param implicit_waiting_time: 隐式等待实践
    :param is_self_closing: 是否自动关闭浏览器
    :return: selenium.webdriver.Chrome()
    """
    try:
        options = webdriver.ChromeOptions()
        if not is_self_closing:
            options.add_experimental_option('detach', True)
        options.add_argument(f'user-data-dir={user_data_path}')

        wd = webdriver.Chrome(options=options)
        wd.implicitly_wait(implicit_waiting_time)
        return wd

    except Exception as e:
        print('Error: ', e)
        traceback.print_exc()


def open_page(wd, page_link):
    """
    :param wd: selenium.webdriver
    :param page_link: https://example.com
    :return:
    """
    try:
        wd.get(page_link)
        time.sleep(2)

    except Exception as e:
        print('Error: ', e)
        traceback.print_exc()
