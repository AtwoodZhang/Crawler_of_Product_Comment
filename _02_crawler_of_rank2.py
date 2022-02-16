# 负责爬虫部分
# 请求html,爬取html中的url
import pymysql
import random
import time
from lxml import etree
import requests
from _00_record_of_agent_pool import ua_list
from _00_record_of_small_functions import *


def crawl_rank2_url(mysql_data, xpath):
    # step1. 检查url是否完整；不完整则补全
    request_url = judge_url_whole2(mysql_data[1])

    # step2. 生成蜘蛛开始爬取
    macy_rank2_spider = MacyRank2Spider(url=request_url, xpath_list=xpath, mysql_data=mysql_data)
    if mysql_data[0] == "gifts & toys":
        try:
            macy_rank2_spider.run()
        except Exception as e:
            print('request错误：', e)

    # step3. 校验爬取对象
    print("xpath:", xpath)
    print("mysql_data:", mysql_data)
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
        url_new = judge_url_whole2(url)
        try:
            self.NETWORK_STATUS = self.support_request(url=url_new, xpath_=self.xpath_list)
        except Exception as e:
            print(e)
            self.NETWORK_STATUS = False
            if self.NETWORK_STATUS is False:
                # 此时是请求超时
                for i in range(1, 5):
                    print('请求超时，第%s次重复请求' % i)
                    self.NETWORK_STATUS = self.support_request(url=url_new, xpath_=self.xpath_list)
        count = 5  # 对同一网页重复五次请求
        while self.NETWORK_STATUS is False and count > 0:
            self.NETWORK_STATUS = self.support_request(url=url, xpath_=self.xpath_list)
            count = count - 1

    def support_request(self, url, xpath_):
        headers = {'User-Agent': random.choice(ua_list)}
        response = requests.get(url=url, headers=headers, timeout=3)
        if response.status_code == 200 and response.text != []:
            response.encoding = "utf-8"
            print(response)
            self.parse_html(response.text, xpath_)
            response.close()
            resp_status = True
        else:
            print("本次请求失败！")
            resp_status = False
        return resp_status

    def parse_html(self, html, xpath_list):
        parse_html = etree.HTML(html)

        # 基准xpath表达式，匹配10个<dd>节点对象
        dd_list = parse_html.xpath(xpath_list[0])
        print("length match:", len(dd_list))
        # 构建item空字典，将提取的数据放入其中
        item = []
        for dd in dd_list:
            # 处理字典数据，注意xpath表达式匹配结果是一个列表，因此需要索引[0]提取数据
            cate_name = dd.xpath(xpath_list[1])[0]
            cate_url = dd.xpath(xpath_list[2])[0]
            item.append((cate_name, cate_url, self.mysql_data[1], self.mysql_data[0]))
        if len(item) > 0:
            self.save_html(item)
            # 更新请求状态
            sql = "update rank1_cate_urls set request_situation='True' where cate_name='{0}';"
            sql = sql.format(self.mysql_data[0])
            print(sql)
            self.cursor.execute(sql)
            self.db.commit()

    def save_html(self, r_list):
        for i in r_list:
            check_if_exist = "SELECT COUNT(*) FROM {0} WHERE cate_url='{1}';"
            check_if_exist = check_if_exist.format('rank2_cate_urls', i[1])
            self.cursor.execute(check_if_exist)

            cnt, = self.cursor.fetchone()
            if cnt == 0:
                sql = "insert ignore into rank2_cate_urls(cate_name, cate_url, upper_cate_url, upper_cate_name) values('{0}','{1}','{2}', '{3}')"
                cate_url = judge_url_whole2(i[1])
                sql = sql.format(i[0], cate_url, i[2], i[3])
                self.cursor.execute(sql)
                self.db.commit()

        time.sleep(random.uniform(1, 3))

    def run(self):
        self.get_html(self.url)

        # 断开游标与数据库链接
        self.cursor.close()
        self.db.close()