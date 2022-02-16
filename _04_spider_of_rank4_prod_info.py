import re
import time
import random
from _03_spider_of_rank3 import MacyRank3Spider


class MacyRank4Info(MacyRank3Spider):
    def parse_html(self, html):
        # step1. 查找本页面需要匹配的对象；
        # # step1.1 查看名字
        # name_re = '<div.*?data-auto="product-name".*?>(.*?)</div>'
        # name_pattern = re.compile(name_re, re.S)
        # name_result = name_pattern.findall(html)
        # print("name_result:", name_result)
        # if len(name_result)>0:
        #     name_result = [name_result[0].strip()]
        #     sql = "update rank4_prod_specific_info set page_prod_name=\"{0}\" where prod_id=\"{1}\";"\
        #         .format(name_result[0], self.mysql_data[0])
        #     sql2 = "update rank4_prod_specific_info set page_prod_name=\'{0}\' where prod_id=\"{1}\";"\
        #         .format(name_result[0], self.mysql_data[0])
        #
        #     print()
        #     try:
        #         print(sql)
        #         self.cursor.execute(sql)
        #         self.db.commit()
        #     except Exception as e:
        #         print(e)
        #         print(sql2)
        #         self.cursor.execute(sql2)
        #         self.db.commit()

        # step1.2 查看价格；
        only_now_price_re = '<div class="lowest-sale-price.*?span class="bold">(.*?)</span>'
        only_now_price_pattern = re.compile(only_now_price_re, re.S)
        only_now_price_result = only_now_price_pattern.findall(html)
        print("only_now:", only_now_price_result)
        if len(only_now_price_result) > 0:
            if len(only_now_price_result)==1:
                result = only_now_price_result[0].strip()
            else:
                result = ''
                for i in only_now_price_result:
                    result = result + '{}'.format(i.strip())
            sql = "update rank4_prod_specific_info set prod_now_price='{0}' where prod_id='{1}';" \
                .format(result, self.mysql_data[0])
            print(sql)
            print()
            self.cursor.execute(sql)
            self.db.commit()
        else:
            now_bef_re = '<div class="lowest-sale-price">.*?class="bold c-red">(.*?)</span.*?</div>.*?class="c-strike">(.*?)</div>'
            now_bef_pattern = re.compile(now_bef_re, re.S)
            now_bef_result = now_bef_pattern.findall(html)
            print("now and before:", now_bef_result)
            if len(now_bef_result) > 0:
                now_bef_result = [i.strip() for i in now_bef_result[0]]
                sql = "update rank4_prod_specific_info set prod_now_price='{0}', prod_before_price='{1}' where prod_id='{2}';" \
                    .format(now_bef_result[0], now_bef_result[1], self.mysql_data[0])
                print(sql)
                print()
                self.cursor.execute(sql)
                self.db.commit()

        # step1.3 查看web_id
        web_re = 'Web ID:(.*?)<'
        web_pattern = re.compile(web_re, re.S)
        web_id_result = web_pattern.findall(html)
        print("web id:", web_id_result)
        if len(web_id_result)>0:
            web_id_result = [web_id_result[0].strip()]
            sql = "update rank4_prod_specific_info set page_web_id='{0}' where prod_id='{1}';".format(web_id_result[0], self.mysql_data[0])
            print(sql)
            print()
            self.cursor.execute(sql)
            self.db.commit()

        time.sleep(random.uniform(1, 3))

        print("this page download well. next beginning!!\n\n")
