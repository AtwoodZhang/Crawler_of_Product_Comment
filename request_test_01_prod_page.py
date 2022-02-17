# use requests to download prod_page

import pymysql
from urllib import request
import re
import time
import random
# from fake_useragent import UserAgent
from request_test_01_UA_agent_pool import ua_list
import requests
from lxml import etree


class MacySpider(object):
    def __init__(self):
        # 初始化属性对象
        self.url = 'https://www.macys.com/'
        # 数据库链接
        self.db = pymysql.connect(
            host="localhost",  # 数据库服务端地址
            user='root',  # 链接数据库所使用的用户名
            passwd='root',  # 数据库密码
            db='macy',  # 数据库名称
            charset='utf8')

        # 创建游标对象
        self.cursor = self.db.cursor()

    def get_header(self):
        # 实例化ua对象
        ua = UserAgent()
        headers = {"User-Agent": ua.random}
        return headers

    def get_html(self, url):
        headers = {'User-Agent': random.choice(ua_list)}
        print("headers:", headers)
        req = requests.get(url=url, headers=headers, timeout=3)
        # req = requests.get(url=url, headers=self.get_header(), timeout=3)
        req.encoding = "utf-8"
        self.parse_html(req.text)

    def parse_html(self, html):
        # xpath = '//*[@id="flexid_1"]/a/span'   # man
        # xpath = '//*[@id="flexid_5991"]/a/span'   # baby
        # href -- xpath:  //*[@id="mainNavigationFobs"]/li/a/@href
        # txt -- xpath:  //*[@id="mainNavigationFobs"]/li/a
        # print(html)
        print('------------------------------------------------------------------------')
        parse_html = etree.HTML(html)
        # 基准xpath表达式，匹配10个<dd>节点对象
        dd_list = parse_html.xpath('//*[@id="mainNavigationFobs"]/li/a')

        print(dd_list)
        # 构建item空字典，将提取的数据放入其中
        item = []
        for dd in dd_list:
            # 处理字典数据，注意xpath表达式匹配结果是一个列表，因此需要索引[0]提取数据
            cate_name = dd.xpath('./span/text()')[0]
            cate_url = dd.xpath('./@href')[0]
            item.append((cate_name, cate_url))
            # 输出数据
            print(item)
        self.save_html(item)

    def save_html(self, r_list):
        sql = "insert into rank_1_url(cate_name, cate_url) values(%s, %s);"
        # 一次性插入多条数据 L:[(),(),()]
        self.cursor.executemany(sql, r_list)
        self.db.commit()

    def run(self):
        url = 'https://www.macys.com/'
        self.get_html(url)
        time.sleep(random.uniform(1, 3))

        # 断开游标与数据库链接
        self.cursor.close()
        self.db.close()


if __name__ == '__main__':
    start = time.time()
    try:
        spider = MacySpider()
        spider.run()
    except Exception as e:
        print('错误：', e)
    end = time.time()
    print("此次耗时：", end-start)
