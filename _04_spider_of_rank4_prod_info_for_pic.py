# step1.4 下载产品图片；直接保存到本地。
import time
import os
from _00_record_of_small_functions import *
from _04_mysql_of_rank4 import MacyRank4Mysql
from concurrent.futures import ThreadPoolExecutor  # 用来构建线程池
import request_test_04_get_comment as rc   # 爬虫
import random
from _00_record_of_agent_pool import ua_list
from _00_record_of_xpath_and_re_dict import xpath_dict
import requests
import pymysql


def run_crawl_img():
    # step1. 从数据库中取出需要request的url；
    r4_img_sql = MacyRank4Mysql()
    r4_img_sql.select_unrequest_prod_img(table_name='rank4_prod_specific_info')
    r4_img_list = [i for i in r4_img_sql.cursor.fetchall()]
    r4_img_sql.database_commit_close()
    print(len(r4_img_list))

    # step1.2. 首先使用一条数据进行测试；
    # r4_img_list = [r4_img_list[21]]
    # r4_img_list = r4_img_list[0:2]
    # print(r4_img_list)
    # print(len(r4_img_list))

    # step2. 对url_list中的每一条数据逐一发送爬取请求；
    # 开启多线程；
    with ThreadPoolExecutor(1) as t:
        for i in r4_img_list:
            case = [i[0], i[2]]
            t.submit(send_request, case)
            time.sleep(random.uniform(1, 3))


def send_request(url_address):
    print(url_address)
    print(url_address[1], url_address[0])
    rc.get_comment(url=url_address[1], x=url_address[0])


if __name__ == "__main__":
    # step1. 写入爬取日志
    log_path = './prod_crawl_log/'
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_file_name = log_path + 'crawl_img_' + 'log-' + time.strftime("%Y%m%d-%H%M%S", time.localtime()) + '.log'
    sys.stdout = Logger(log_file_name)
    sys.stderr = Logger(log_file_name)

    # step2. 运行爬取过程；
    start = time.time()
    run_crawl_img()
    end = time.time()
    spend_time = end - start
    print("finish crawl prod_img：", spend_time)
