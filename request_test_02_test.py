# step1, select rank1 url from mysql;
# step2, select first to request rank2 url;

import pymysql
import random
import time
from lxml import etree
import requests
from request_test_00_xpath_dict import xpath_dict
import request_test_02_cate_page as rt02


def step1():
    # rank1 url 保存在root:Macy:rank_1_url
    db = pymysql.connect(
        host="localhost",  # 数据库服务端地址
        user='root',  # 链接数据库所使用的用户名
        passwd='root',  # 数据库密码
        db='macy',  # 数据库名称
        charset='utf8')
    cursor = db.cursor()


def man_requests_rank2_url(mysql_data):
    xpath_use = xpath_dict['url_rank2'][mysql_data[1]]
    print(xpath_use)
    print(mysql_data)
    return xpath_use


def requests_url(mysql_data):
    # 数据类型：
    # (14, 'Gifts & Toys',
    # '/shop/holiday-gift-guide?id=101254&cm_sp=us_hdr-_-gifts-%26-toys-_-101254_gifts-%26-toys',None)
    if mysql_data[1] != 'Men':
        pass
    elif mysql_data[1] == 'Men':
        xpath_use = man_requests_rank2_url(mysql_data)
    else:
        pass


if __name__ == "__main__":
    rt02.run()