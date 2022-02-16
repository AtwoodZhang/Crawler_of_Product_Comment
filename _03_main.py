import time
import random
from _00_record_of_xpath_and_re_dict import *
from _03_mysql_of_rank3 import MacyRank3Mysql
from _03_spider_of_rank3 import MacyRank3Spider
from concurrent.futures import ThreadPoolExecutor  # 用来构建线程池


def run():
    # step1. 从数据库中取出需要request的url；
    r3_sql = MacyRank3Mysql()
    r3_sql.select_upper_no_request(table_name='rank2_cate_urls')
    r2_mysql_list = [i for i in r3_sql.cursor.fetchall()]
    r3_sql.database_commit_close()

    # step1.2. 首先使用一条数据进行测试；
    # r2_mysql_list = [r2_mysql_list[21]]
    # print(r2_mysql_list)
    # print(len(r2_mysql_list))

    # step2. 对url_list中的每一条数据逐一发送爬取请求；
    # 开启多线程；
    with ThreadPoolExecutor(30) as t:
        for i in r2_mysql_list:
            t.submit(send_request, i)
            # time.sleep(random.uniform(1, 3))


def send_request(mysql_data):
    m3_spider = MacyRank3Spider(url=mysql_data[3], match_list=re_dict['rank3'], mysql_data=mysql_data)
    m3_spider.run()


if __name__ == "__main__":
    start = time.time()
    run()
    end = time.time()
    spend_time = end - start
    print("爬取rank3结束：", spend_time)