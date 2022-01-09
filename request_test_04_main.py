# step1. 从数据库中取出需要请求的url，即未认为是已经请求过的url
# step2. 构建线程池，完成任务；
# step3. 任务部署：
#        1) 制作xpath,填写comment字典；
#        2) 对step1取出的每一个url,发送requests.
#        3) 对requests返回的每一个response匹配xpath。
#        4) 存储response匹配结果。
import pymysql
import requests
from request_test_01_UA_agent_pool import ua_list
from concurrent.futures import ThreadPoolExecutor  # 用来构建线程池
from request_test_04_get_comment import get_comment
from request_test_03_mysql import MysqlRank3


def step1_get_url():
    r3_sql = MysqlRank3()
    r3_sql.select_rank2_all(table_name='rank_3_url')
    r4_url_list = [i for i in r3_sql.cursor.fetchall()]
    r3_sql.database_commit_close()
    print(len(r4_url_list))
    print(r4_url_list[0])
    url_list = r4_url_list[0]
    return url_list


def main_request():
    url_list_0 = step1_get_url()

    # step1. 统一url的格式，是可以直接访问的格式；
    url_list_copy = url_list_0
    for i in range(len(url_list_copy)):
        if url_list_copy[i][3] == '/' or url_list_copy[i][3] != 'h':
            url_list_copy[i][3] = "https://www.macys.com" + url_list_copy[i][3]

    # step2. 有了所有产品的url.逐一请求具体产品页中的评论。首先构建线程池。提交任务。
    with ThreadPoolExecutor(50) as t:
        for i in url_list_copy:
            t.submit(get_comment, i[3])


if __name__ == "__main__":
    main_request()
    # step1_get_url()