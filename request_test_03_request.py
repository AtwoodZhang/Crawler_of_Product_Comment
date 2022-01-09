from request_test_02_crawl_rank2 import MacyRank2Spider
import time
import random
import requests
from request_test_01_UA_agent_pool import ua_list
from lxml import etree
import pymysql
import re


class MacyRank3Spider(object):
    def __init__(self, url, xpath_list, mysql_data):
        # MacyRank3Spider(url=i[3], xpath_list=xpath_list, mysql_data=r3_url_list2)
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
        if url[0] == '/' or url[0] != 'h':
            url_new = 'https://www.macys.com' + url
        elif isinstance(url, list):
            url_new = url[0]
        else:
            url_new = url

        print('now: url new:')
        print(url_new)

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

        count = 5
        while self.NETWORK_STATUS is False and count > 0:
            self.NETWORK_STATUS = self.support_request(url=url, xpath_=self.xpath_list)
            count = count - 1

    def support_request(self, url, xpath_):
        headers = {'User-Agent': random.choice(ua_list)}
        response = requests.get(url=url, headers=headers, timeout=3)
        # print(response.text)
        resp_status = False
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
        # print(parse_html)
        dd_list = parse_html.xpath(xpath_list[0])
        print(xpath_list[0])

        item = []
        print("dd_list.length:", len(dd_list))
        print(dd_list)
        for dd in dd_list:
            # 处理字典数据，注意xpath表达式匹配结果是一个列表，因此需要索引[0]提取数据
            cate_name = dd.xpath(xpath_list[2])[0].strip()
            cate_url = dd.xpath(xpath_list[1])[0].strip()
            sql_insert = self.mysql_data[1] + '_' + self.mysql_data[2]
            if cate_url[0] == '/' or cate_url[0] != 'h':
                cate_url = "https://www.macys.com" + cate_url
            item.append((cate_name, cate_url, sql_insert))
            # 输出数据
        print(len(item))
        print('item:', item)

        re_string2 = '<div class="productDescription".*?a href="(.*?)" title="(.*?)" class="productDescLink".*?>'
        pattern1 = re.compile(re_string2, re.S)
        result1 = pattern1.findall(html)
        item_re = []
        sql_insert = self.mysql_data[1] + '_' + self.mysql_data[2]
        for i in result1:
            # print(i)
            i_0 = i[0]
            i_0 = i_0.strip()
            i_1 = i[1]
            i_1 = i_1.strip()
            if i_0[0] == '/' or i_0[0] != 'h':
                i_0 = "https://www.macys.com" + i_0
            item_re.append((i_1, i_0, sql_insert))
        print(len(item_re))
        print("item_re", item_re)
        # print('result1:', result1)
        self.save_html(item_re)
        # 检查下一页：
        print("This page downloaded well.")
        next_page_string = '<div class="icon-ui-chevron-right-gr-huge".*?a href="(.*?)" aria-label=.*?Go forward to page.*?>'
        next_page_pattern = re.compile(next_page_string, re.S)
        result_next_page = next_page_pattern.findall(html)
        if result_next_page != [] and len(result_next_page) == 1 \
                and (result_next_page[0] == '/' or result_next_page[0] != 'h'):
            result_next_page[0] = "https://www.macys.com" + result_next_page[0]
        print('next_page:', result_next_page)
        # next_url_page = parse_html.xpath(xpath_list[3])
        while result_next_page:
            self.get_html(result_next_page[0])
        # # 更新请求
        sql = "update rank_2_url set request_situation='True' where cate_url='{0}';".format(self.url)
        self.cursor.execute(sql)
        self.db.commit()

    def save_html(self, r_list):
        for i in r_list:
            check_if_exist = "SELECT COUNT(*) FROM {0} WHERE cate_url='{1}';"
            check_if_exist = check_if_exist.format('rank_3_url', i[1])
            print(check_if_exist)
            self.cursor.execute(check_if_exist)

            cnt, = self.cursor.fetchone()
            print(cnt)
            if cnt == 0:

                sql = 'insert ignore into rank_3_url(cate_name, cate_url, up_url_name) values("{0}", "{1}", "{2}");'
                sql = sql.format(i[0], i[1], i[2])
                print(sql)
                self.cursor.execute(sql)
                self.db.commit()
        time.sleep(random.uniform(1, 4))

    def run(self):
        self.get_html(self.url)
        # 断开游标与数据库链接
        self.cursor.close()
        self.db.close()
