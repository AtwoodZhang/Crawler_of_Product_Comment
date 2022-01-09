# 负责爬虫部分
# 请求html,爬取html中的url
import pymysql
import random
import time
from lxml import etree
import requests
from request_test_01_UA_agent_pool import ua_list


def find_url_need_to_request(request_url, xpath, mysql_data):
    macy_rank2_spider = MacyRank2Spider(url=request_url, xpath_list=xpath, mysql_data=mysql_data)
    check_if_requested = "select cate_name from rank_1_url where request_situation <> 'True' or request_situation is NULL;"
    # print(check_if_requested)
    macy_rank2_spider.cursor.execute(check_if_requested)
    need_to_request = []
    need_to_request_tuple = macy_rank2_spider.cursor.fetchall()
    print("need to request:", need_to_request)
    macy_rank2_spider.db.commit()
    macy_rank2_spider.cursor.close()
    macy_rank2_spider.db.close()
    for i in need_to_request_tuple:
        need_to_request.append(i[0])
    return need_to_request


def crawl_rank2_url(mysql_data, xpath):
    start_url = 'https://www.macys.com'
    request_url = start_url + mysql_data[2]
    print("**************************************************************************************")
    # 查找还有哪些二级url没有请求到；
    url_list = find_url_need_to_request(request_url, xpath, mysql_data)
    print(url_list)
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

    # if mysql_data[1] in url_list:
    if mysql_data[1] == 'Gifts & Toys':
        macy_rank2_spider = MacyRank2Spider(url=request_url, xpath_list=xpath, mysql_data=mysql_data)
        try:
            macy_rank2_spider.run()
        except Exception as e:
            print('request错误：', e)

    print(request_url)
    print(xpath)
    print()


class MacyRank2Spider(object):
    def __init__(self, url, xpath_list, mysql_data):
        # 初始化属性对象
        self.url = url
        # 创建xpath
        self.xpath_list = xpath_list
        # 保存上级name
        self.mysql_data = mysql_data
        # 数据库链接
        self.db = pymysql.connect(
            host="localhost",  # 数据库服务端地址
            user='root',  # 链接数据库所使用的用户名
            passwd='root',  # 数据库密码
            db='macy',  # 数据库名称
            charset='utf8')
        # 创建游标对象
        self.cursor = self.db.cursor()
        # 网络返回状态
        self.NETWORK_STATUS = True

    def get_html(self, url):
        self.NETWORK_STATUS = False
        try:
            headers = {'User-Agent': random.choice(ua_list)}
            response = requests.get(url=url, headers=headers, timeout=3)
            if response.status_code == 200:
                print("headers:", headers)
                self.NETWORK_STATUS = True
                response.encoding = "utf-8"
                self.parse_html(response.text, self.xpath_list)
        except Exception as e:
            print(e)
            self.NETWORK_STATUS = False
            if self.NETWORK_STATUS is False:
                '''此时是请求超时'''
                for i in range(1, 5):
                    print('请求超时，第%s次重复请求' % i)
                    headers = {'User-Agent': random.choice(ua_list)}
                    response = requests.get(url=url, headers=headers, timeout=3)
                    if response.status_code == 200:
                        self.NETWORK_STATUS = True
                        response.encoding = "utf-8"
                        self.parse_html(response.text, self.xpath_list)
        if self.NETWORK_STATUS is False:
            # 存储失败url
            print(self.url, "该url请求失败！")

    def parse_html(self, html, xpath_list):
        parse_html = etree.HTML(html)
        # 基准xpath表达式，匹配10个<dd>节点对象
        dd_list = parse_html.xpath(xpath_list[0])
        # 更新请求
        self.update_success_request_url(self.url, self.mysql_data[1])
        # print(dd_list)
        # 构建item空字典，将提取的数据放入其中
        item = []
        for dd in dd_list:
            # 处理字典数据，注意xpath表达式匹配结果是一个列表，因此需要索引[0]提取数据
            cate_name = dd.xpath(xpath_list[1])[0]
            cate_url = dd.xpath(xpath_list[2])[0]
            item.append((cate_name, cate_url, self.mysql_data[1]))
            # 输出数据
        print(len(item))
        self.save_html(item)

    def update_false_request_url(self, url, name):
        sql = "update rank_1_url set request_situation='False' where cate_name='{}';".format(name)
        print(sql)
        self.cursor.execute(sql)
        # self.db.commit()

    def update_success_request_url(self, url, name):
        sql = "update rank_1_url set request_situation='True' where cate_name='{}';".format(name)
        print(sql)
        self.cursor.execute(sql)
        # self.db.commit()

    def save_html(self, r_list):
        check_if_exist = "SELECT COUNT(*) from `{0}` where cate_url = \"{1}\""
        check_if_exist = check_if_exist.format('rank_2_url', r_list[0][1])
        self.cursor.execute(check_if_exist)
        # print(check_if_exist)

        cnt, = self.cursor.fetchone()
        if cnt == 0:
            sql = "insert ignore into rank_2_url(cate_name, cate_url, up_url_name) values(%s, %s, %s);"
            # 一次性插入多条数据 L:[(),(),()]
            self.cursor.executemany(sql, r_list)
            self.db.commit()

        time.sleep(random.uniform(1, 3))

        # 断开游标与数据库链接
        self.cursor.close()
        self.db.close()

    def run(self):
        self.get_html(self.url)
