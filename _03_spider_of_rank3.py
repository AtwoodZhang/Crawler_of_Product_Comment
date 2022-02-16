import requests
import pymysql
import random
import time
from _00_record_of_small_functions import *
from _00_record_of_agent_pool import ua_list
import re


class MacyRank3Spider(object):
    # rank3测试的时候一直没办法使用xpath爬取成功，因此使用了re模块，同时爬虫初始化的时候不初始化xpath
    def __init__(self, url, match_list, mysql_data):
        self.url = url
        self.match_list = match_list
        self.mysql_data = mysql_data
        self.parse_status = True
        self.db = pymysql.connect(
            host="localhost",
            user="root",
            passwd='root',
            db='macy',
            charset='utf8')
        self.cursor = self.db.cursor()

    def get_html(self, url):
        url_new = judge_url_whole2(url)
        try:
            network_status = self.support_request(url=url_new)
        except Exception as e:
            print(e)
            network_status = False
            if network_status is False:
                # 此时是请求超时
                for i in range(1, 5):
                    print('请求超时，第%s次重复请求' % i)
                    network_status = self.support_request(url=url_new)
        count = 10  # 重复10次请求
        while network_status is False and count > 0:
            network_status = self.support_request(url=url_new)
            count = count - 1

    def support_request(self, url):
        headers = {'User-Agent': random.choice(ua_list)}
        response = requests.get(url=url, headers=headers, timeout=3)
        if response.status_code == 200 and response.text != []:
            response.encoding = "utf-8"
            print(response)
            self.parse_html(response.text)
            response.close()
            resp_status = True
        else:
            print("本次请求失败！")
            resp_status = False
        return resp_status

    def parse_html(self, html):
        # step1. 查找本页面需要匹配的对象；

        # step1.1 查看名字、链接
        href_title_re = '<div class="productDescription".*?a href="(.*?)" title="(.*?)" class="productDescLink".*?>'
        href_title_pattern = re.compile(href_title_re, re.S)
        href_title_result = href_title_pattern.findall(html)
        if len(href_title_result) == 0:
            self.parse_status = False
        else:
            self.parse_status = True
        href_title_item = []
        upper_name_insert = self.mysql_data[1]+'_'+self.mysql_data[2]
        for i in href_title_result:
            cate_url = i[0]
            cate_url = cate_url.strip()
            cate_name = i[1]
            cate_name = cate_name.strip()
            cate_url = judge_url_whole2(cate_url)
            # print(cate_url)
            href_title_item.append((cate_name, cate_url, upper_name_insert, self.url))

        # step1.2 查看价格
        before_price_re = ''
        now_price_re = ''

        print("length of title and href(match re):", len(href_title_item))

        # step2.查找结果数目大于零，保存，并向下一页发送请求
        if len(href_title_item) > 0:
            self.save_html(href_title_item)
            print("This page downloaded well.")

            # step2.1 检查是否存在下一页；
            next_page_string = '<div class="icon-ui-chevron-right-gr-huge".*?a href="(.*?)" aria-label=.*?Go forward to page.*?>'
            next_page_pattern = re.compile(next_page_string, re.S)
            next_page_url = next_page_pattern.findall(html)
            if next_page_url != [] and len(next_page_url) == 1:
                next_page_url = judge_url_whole2(next_page_url[0])
            while next_page_url:
                self.get_html(next_page_url)
                if self.parse_status is False:
                    break

            # step2.2 更新请求
            sql = "update rank2_cate_urls set request_situation='True' where cate_url='{0}';".format(self.url)
            self.cursor.execute(sql)
            self.db.commit()

    def save_html(self, r_list):
        for i in r_list:
            check_if_exist = "SELECT COUNT(*) FROM {0} WHERE cate_url='{1}';"
            check_if_exist = check_if_exist.format('rank3_cate_urls', i[1])
            self.cursor.execute(check_if_exist)

            cnt, = self.cursor.fetchone()
            if cnt == 0:
                sql = 'insert ignore into rank3_cate_urls(cate_name, cate_url, upper_cls_name, upper_cate_url) ' \
                      'values("{0}", "{1}", "{2}", "{3}");'
                cate_url = judge_url_whole2(i[1])
                sql = sql.format(i[0], cate_url, i[2], i[3])
                self.cursor.execute(sql)
                self.db.commit()

        time.sleep(random.uniform(1, 3))

    def run(self):
        self.get_html(self.url)
        self.cursor.close()
        self.db.close()
