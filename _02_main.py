from _02_get_rank2_xpath import get_xpath_name2
from _02_crawler_of_rank2 import crawl_rank2_url
import pymysql
import time


def run():
    # 1. 链接数据库，提取所有需要访问的url
    db = pymysql.connect(
        host="localhost",  # 数据库服务端地址
        user='root',  # 链接数据库所使用的用户名
        passwd='root',  # 数据库密码
        db='macy',  # 数据库名称
        charset='utf8')
    cursor = db.cursor()
    sql = "select * from rank1_cate_urls where request_situation is NULL or request_situation <> 'True';"
    cursor.execute(sql)

    # 2. 显示取出的表数据的结构
    col_name_list = [a[0] for a in cursor.description]
    print("mysql category: ", col_name_list)

    rank1_list = []
    # step0. 连接数据库，得到url
    one_mysql = cursor.fetchone()
    while one_mysql is not None:
        # step1. 得到一条mysql数据，有当前页面url
        rank1_list.append(one_mysql)

        # step2. 根据url，算出xpath,根据mysql一条数据，得到对应要获取的xpath
        xpath_use = get_xpath_name2(one_mysql)

        # step3. 根据mysql的数据，和xpath,爬取rank3的url;
        crawl_rank2_url(one_mysql, xpath_use)

        # step4. 获取下一条mysql数据；
        one_mysql = cursor.fetchone()
        print("\nnext page begins to download.")

    db.commit()
    db.close()


if __name__ == "__main__":
    start = time.time()
    run()
    end = time.time()
    print("二级url消耗时间：", end - start)
