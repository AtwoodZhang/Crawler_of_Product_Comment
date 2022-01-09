import pymysql
# import request_test_03_mysql as r3_sql
import time
from request_test_03_mysql import MysqlRank3
from request_test_03_request import MacyRank3Spider
from request_test_00_xpath_dict import xpath_dict
from concurrent.futures import ThreadPoolExecutor  # 用来构建线程池


# step1. 逐一从数据库中取出需要request的url；
def run():
    # 提取未请求url地址
    # r3_sql.select_rank2_urls(table_name='rank_2_url', cate_name='cate_url')
    # r3_url_list = [i[0] for i in r3_sql.cursor.fetchall()]
    # print(r3_url_list)
    # r3_sql.database_commit_close()
    r3_sql2 = MysqlRank3()
    r3_sql2.select_rank2_all(table_name='rank_2_url')
    r3_url_list2 = [i for i in r3_sql2.cursor.fetchall()]
    r3_sql2.database_commit_close()
    # 先用一条数据进行测试
    r3_url_list3 = [r3_url_list2[0]]
    print(r3_url_list3)

    # 对每一条数据逐一开始发送爬取请求
    for i in r3_url_list3:
        # 初始化request
        # print(i)
        x_dict_page = xpath_dict['url_rank3']
        xpath_list = [x_dict_page['product'], x_dict_page['href'], x_dict_page['cate_name'], x_dict_page['next_page']]
        print("xpath:", xpath_list)
        m3_spider = MacyRank3Spider(url=i[3], xpath_list=xpath_list, mysql_data=i)
        m3_spider.run()


if __name__ == "__main__":
    start = time.time()
    run()
    end = time.time()
    spend_time = end - start
    print("爬取rank3结束：", spend_time)

    # with ThreadPoolExecutor(50) as t:
    #     t.submit(# 任务， # 参数)


