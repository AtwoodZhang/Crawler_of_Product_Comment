import time
import random
import os
import sys
from _00_record_of_small_functions import *
from _03_spider_of_rank3 import MacyRank3Spider
from _04_mysql_of_rank4 import MacyRank4Mysql
from concurrent.futures import ThreadPoolExecutor  # 用来构建线程池
# from _04_spider_of_rank4_review_write_txt import MacyRank4Write
from _04_spider_of_rank4_prod_info import MacyRank4Info


def run():
    # step1. 从数据库中取出需要request的url；
    r4_info_sql = MacyRank4Mysql()
    r4_info_sql.select_info_no_request_url4(table_name='rank4_prod_specific_info', cate_name='prod_now_price')
    r4_info_list = [i for i in r4_info_sql.cursor.fetchall()]
    r4_info_sql.database_commit_close()
    print(len(r4_info_list))

    # step1.2. 首先使用一条数据进行测试；
    # r4_info_list = [r4_info_list[21]]
    # print(r4_info_list)
    # print(len(r4_info_list))

    # step2. 对url_list中的每一条数据逐一发送爬取请求；
    # 开启多线程；
    with ThreadPoolExecutor(1) as t:
        for i in r4_info_list:
            t.submit(send_request, i)
            # time.sleep(random.uniform(1, 3))


def send_request(one_mysql_data):
    match_list = ''
    url = one_mysql_data[2]
    m4_write_spider = MacyRank4Info(url=url, match_list=match_list, mysql_data=one_mysql_data)
    m4_write_spider.run()


if __name__ == "__main__":
    # step1. 写入爬取日志
    log_path = './prod_crawl_log/'
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_file_name = log_path + 'log-' + time.strftime("%Y%m%d-%H%M%S", time.localtime()) + '.log'
    sys.stdout = Logger(log_file_name)
    sys.stderr = Logger(log_file_name)

    # step2. 主函数
    start = time.time()
    run()
    end = time.time()
    print('this running action cost {} seconds'.format(end-start))