import time
import os
import sys
import random
from _00_record_of_small_functions import *
from _04_mysql_of_rank4 import MacyRank4Mysql
from concurrent.futures import ThreadPoolExecutor  # 用来构建线程池
from _04_spider_of_rank4_review_write_txt import MacyRank4Write

name_count_1 = 1  # 线程
name_count_2 = 1  # 请求次数

# def run():
#     # step1. 从数据库中取出需要request的url；
#     r4_sql = MacyRank4Mysql()
#     r4_sql.select_upper_no_request(table_name='rank3_cate_urls')
#     r3_mysql_list = [i for i in r4_sql.cursor.fetchall()]
#     r4_sql.database_commit_close()
#     print(len(r3_mysql_list))
#
#     # step1.2. 首先使用一条数据进行测试；
#     # r2_mysql_list = [r2_mysql_list[21]]
#     # print(r2_mysql_list)
#     # print(len(r2_mysql_list))
#
#     # step2. 对url_list中的每一条数据逐一发送爬取请求；
#     # 开启多线程；
#     with ThreadPoolExecutor(10) as t:
#         for i in r3_mysql_list:
#             t.submit(send_request, i)
#             time.sleep(random.uniform(1, 3))
#
#
# def send_request(url_address):
#     m4_write_spider = MacyRank4Write(url=url_address)
#     m4_write_spider.run()


def run_write_review():
    # step1. 从数据库中取出需要request的url；
    r4_sql = MacyRank4Mysql()
    r4_sql.select_upper_no_request(table_name='rank4_prod_specific_info')
    id_mysql_list = [i for i in r4_sql.cursor.fetchall()]
    r4_sql.database_commit_close()
    print("id_mysql_list length: ", len(id_mysql_list))

    # step1.2 测试一条数据
    # id_mysql_list = id_mysql_list[1:5]

    # step2. 对url_list中的每一条数据逐一发送爬取请求；
    # 开启多线程；
    with ThreadPoolExecutor(40) as t:
        for i in id_mysql_list:
            print("mysql_data(in thread):", i)
            t.submit(send_request, i)
            global name_count_1
            name_count_1 = name_count_1+1
            time.sleep(random.uniform(1, 2)) # 不随机休眠，因为write本身花费了一定的时间


def send_request(one_mysql_data):
    # step1. 尝试发起第一次评论请求；
    # print(one_mysql_data)
    url_address = "https://www.macys.com/xapi/digital/v1/product/{}/reviews?_shoppingMode=SITE&_regionCode=US" \
                  "&currencyCode=USD&_customerState=GUEST&_deviceType=DESKTOP&sort=NEWEST&limit=8"
    url_address = url_address.format(one_mysql_data[0])
    print("url_address: ", url_address)
    global name_count_1, name_count_2
    name_count1 = str(name_count_1).zfill(8) + "_" + str(name_count_2).zfill(8)
    m4_write_spider = MacyRank4Write(url=url_address, prod_id=one_mysql_data[0], name_count=name_count1)
    resp = m4_write_spider.run()
    print(resp)
    name_count_2 = name_count_2 + 1

    # step2. 若第一次请求成功，则尝试发起第二次请求；
    offset = 8
    while resp is True:
        url_address = "https://www.macys.com/xapi/digital/v1/product/{0}/reviews?_shoppingMode=SITE&_regionCode=US" \
                      "&currencyCode=USD&_customerState=GUEST&_deviceType=DESKTOP&sort=NEWEST&limit=30&offset={1}"
        url_address = url_address.format(one_mysql_data[0], offset)
        print("url_address_while: ", url_address)
        name_count1 = str(name_count_1).zfill(8) + "_" + str(name_count_2).zfill(8)
        m4_write_spider = MacyRank4Write(url=url_address, prod_id=one_mysql_data[0], name_count=name_count1)
        resp = m4_write_spider.run()
        offset = offset + 30
        name_count_2 = name_count_2 + 1

    r4_sql = MacyRank4Mysql()
    r4_sql.update_rank4_request_situation(table_name='rank4_prod_specific_info', prod_id=one_mysql_data[0])
    r4_sql.database_commit_close()


if __name__ == "__main__":

    # step1. 写入爬取日志
    log_path = './prod_crawl_log/'
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_file_name = log_path + 'log-' + time.strftime("%Y%m%d-%H%M%S", time.localtime())+'.log'
    sys.stdout = Logger(log_file_name)
    sys.stderr = Logger(log_file_name)

    # step2. 运行爬取过程；
    start = time.time()
    run_write_review()
    end = time.time()
    spend_time = end - start
    print("finish crawl rank4：", spend_time)


