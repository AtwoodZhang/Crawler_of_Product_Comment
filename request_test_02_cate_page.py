import pymysql
import random
import time
from lxml import etree
import requests
from request_test_01_UA_agent_pool import ua_list
from request_test_02_crawl_rank2 import crawl_rank2_url


def normal_cope(case):  # man, woman等的爬取url方法；
    print(case, '-->  case_normal_cope')
    xpath_rank1 = '//*[@id="row_1"]/ul/li/div/a'
    xpath_rank2_name = './picture/img/@alt'
    xpath_rank2_url = './@href'
    xpath_list = [xpath_rank1, xpath_rank2_name, xpath_rank2_url]
    return xpath_list


def toy_and_gift(case):
    print(case, '-->  case_toy')
    xpath_rank1 = '//*[@id="bodyContainer"]/div/section[2]/div/div/div[2]/div/a'
    xpath_rank2_name = './@id'
    xpath_rank2_url = './@href'
    xpath_list = [xpath_rank1, xpath_rank2_name, xpath_rank2_url]
    return xpath_list


def trending(case):
    print(case, '-->  case_trending')
    xpath_rank1 = '//*[@id="get-inspired"]/section/div/div/div/a'
    xpath_rank2_name = './button/text()'
    xpath_rank2_url = './@href'
    xpath_list = [xpath_rank1, xpath_rank2_name, xpath_rank2_url]
    return xpath_list


def sale(case):
    print(case, '-->  case_sale')
    xpath_rank1 = '//*[@id="row_0"]/ul/li/div/div/a'
    xpath_rank2_name = './div/div/h3/text()'
    xpath_rank2_url = './@href'
    xpath_list = [xpath_rank1, xpath_rank2_name, xpath_rank2_url]
    return xpath_list


def other(case):
    print('this case', case, 'is wrong!')


def get_xpath(mysql_data):
    # print(mysql_data[1])
    dict_func = {
        'Gifts & Toys': toy_and_gift,
        'Women': normal_cope,
        'Men': normal_cope,
        'Kids & Baby': normal_cope,
        'Beauty': normal_cope,
        'Home': normal_cope,
        'Furniture ': normal_cope,
        'Shoes': normal_cope,
        'Jewelry': normal_cope,
        'Handbags & Accessories': normal_cope,
        'Now Trending': trending,
        'Sale': sale
    }
    method = dict_func.get(mysql_data[1], other)
    if method:
        xpath_use = method(mysql_data[1])
        print(mysql_data[1])
        return xpath_use
    return False


def run():
    db = pymysql.connect(
        host="localhost",  # 数据库服务端地址
        user='root',  # 链接数据库所使用的用户名
        passwd='root',  # 数据库密码
        db='macy',  # 数据库名称
        charset='utf8')
    cursor = db.cursor()
    sql = "select * from rank_1_url"
    cursor.execute(sql)
    # print("a f:", cursor.description)
    col_name_list = [a[0] for a in cursor.description]
    print("mysql category: ", col_name_list)

    rank1_list = []

    # step0. 连接数据库，得到url
    one = cursor.fetchone()
    while one is not None:
        # step1. 得到一条mysql数据，有当前页面url
        rank1_list.append(one)

        # step2. 根据url，算出xpath,根据mysql一条数据，得到对应要获取的xpath
        # print(one)
        xpath_use = get_xpath(one)
        # print(xpath_use)

        # step3. 根据mysql的数据，和xpath,爬取rank3的url;
        crawl_rank2_url(one, xpath_use)

        # step4. 获取下一条mysql数据；
        one = cursor.fetchone()
    db.commit()
    db.close()


if __name__ == "__main__":
    start = time.time()
    run()
    end = time.time()
    print("二级url消耗时间：", end - start)
