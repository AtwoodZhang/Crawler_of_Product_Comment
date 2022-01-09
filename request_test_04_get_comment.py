import requests
import pymysql
from request_test_01_UA_agent_pool import ua_list
from request_test_00_xpath_dict import xpath_dict
import random
from lxml import etree
import time
import msvcrt
import re
from request_test_04_mysql import MysqlRank4


def get_comment(url):
    # url表示requests的具体html页
    comment_xpath = xpath_dict['url_rank4']
    resp_status = False
    try:
        resp_status = support_request(url=url, xpath_=comment_xpath)
    except Exception as e:
        print(e)
        # 此时是请求超时
        for i in range(1, 5):
            print('请求超时，第%s次重复请求' % i)
            resp_status = support_request(url=url, xpath_=comment_xpath)

    # 若解析失败则多次请求
    count = 0
    if resp_status is False:
        count = 5
    while resp_status is False and count > 0:
        resp_status = support_request(url=url, xpath_=comment_xpath)
        count = count - 1


def support_request(url, xpath_):
    headers = {'User-Agent': random.choice(ua_list)}
    response = requests.get(url=url, headers=headers, timeout=3)
    # print(response.text)
    resp_status = False
    if response.status_code == 200 and response.text != []:
        response.encoding = "utf-8"
        parse_html(response.text, xpath_, url)
        response.close()
        resp_status = True
    else:
        print("本次请求失败！")
        resp_status = False
    return resp_status


def parse_html(html_, xpath_, url):
    # xpath_ 需要的存储方法：
    # 1）商品信息：
    # 2）
    # 3）next_page: //*[@id="BVRRContainer"]/div/div[3]/div/div[2]/ul/li[3]/button
    #               next page 用的是动态包，需要抓动态包
    parse_html1 = etree.HTML(html_)

    # test1. 使用xpath进行尝试。怎么匹配都匹配不上。很烦！
    # print(parse_html1)
    # prod_desc = parse_html1.xpath('//*[@id="mainCont"]/div[2]/div[2]/div/div/div[1]/div/div[2]/div')
    # prod_desc_series = prod_desc[0].xpath('./div[@data-el="header"]/div/div[@data-el="product-title"]/h1/a/text()')
    # prod_desc_name = prod_desc[0].xpath('./div[@data-el="header"]/div/div[@data-el="product-title"]/h1/div/text()')
    # prod_desc_name = parse_html1.xpath('//*[@id="mainCont"]/div[2]/div[2]/div/div/div[1]/div/div[2]/div/div[@data-el="header"]/div/div[@data-el="product-title"]/h1/div/text()')
    # prod_desc_cost = prod_desc[0].xpath(
    # './div[@data-el="order-panel"]/div/div/div/div/div[@data-el="price"]/div/h3/div')
    # prod_img = parse_html1.xpath(
    #     '//*[@id="mainCont"]/div[2]/div[2]/div/div/div[1]/div/div[1]/div/div/div/div/div/div[3]/div/div/div/div/div/picture[@class="main-picture"]/img/@src')
    # prod_img 一共四个链接或者三个链接
    # print("产品描述：", prod_desc)
    # print("产品系列：", prod_desc_series)
    # print("产品名：", prod_desc_name)
    # print("产品价格：", prod_desc_cost)
    # print("产品图片系列：", prod_img)

    # test2. 使用re匹配。
    # 1) 价格
    now_price_re = \
        '<h3 class="tiered-prices h3 redesign-temp".*?div class="lowest-sale-price".*?span class=.*?>(.*?)</span>'
    before_price_re = '<div class="c-strike">(.*?)</div>'
    price_now_pattern = re.compile(now_price_re, re.S)
    price_before_pattern = re.compile(before_price_re, re.S)
    price_now = [price_now_pattern.findall(parse_html1)[0].strip()]
    price_before = [price_before_pattern.findall(parse_html1)[0].strip()]

    # 2) 商品名：
    prod_name = '<div class="product-title" data-auto="product-name" itemprop="name".*?>(.*?)</div>'
    prod_name_pattern = re.compile(prod_name, re.S)
    name_page = [prod_name_pattern.findall(f3)[0].strip()]

    # 3) WebID:
    web_id_string = '<p class="c-margin-bottom-4v web-id c-legal".*?Web ID:(.*?)</p>'
    web_id_pattern = re.compile(web_id_string, re.S)
    result_web_id = [web_id_pattern.findall(parse_html1)[0].strip()]

    # 4) url为输入；
    # 5) image在comment中有链接，不过page中的image尺寸更大。
    re_string_rank4_img = '<div class="media-wrapper image-grid-wrapper".*?class="main-picture">.*?<source type="image/webp" srcset="(.*?)">'
    pattern4 = re.compile(re_string_rank4_img, re.S)
    img_url = [pattern4.findall(parse_html1)[0].strip()]

    print("before_price", price_before)
    print("now_price", price_now)
    print('name:', name_page)
    print('web_id:', result_web_id)
    print("img_url:", img_url)

    prod_mysql = MysqlRank4()
    prod_mysql.new_prod_message_insert(result_web_id, img_url, url, price_before, price_now)
    prod_mysql.database_commit_close()


def request_static(url):
    # 1. 查看package的url.
    #    1) 产品1.
    #    2) 评价：1) 评语：//*[@id="BVRRContainer"]/div/div[2]/div/div/ul/li/div/div/span/div/text()
    #            2）评语details: //*[@id="BVRRContainer"]/div/div[2]/div/div/ul/li/div/div/div/div/p/text()
    #            3) 评论人：//*[@id="BVRRContainer"]/div/div[2]/div/div/ul/li/div/div/div/text()
    #            4) comment next_page://*[@id="BVRRContainer"]/div/div[3]/div/div[2]/ul/li[3]/button
    # 2.
    pass


def request_package(url):
    # 1. package url:
    # prod_1
    # page2
    # https://www.macys.com/xapi/digital/v1/product/12614577/reviews?_shoppingMode=SITE&_regionCode=US&currencyCode=USD&_customerState=GUEST&_deviceType=DESKTOP&sort=NEWEST&limit=30&offset=8
    # page1
    # https://www.macys.com/xapi/digital/v1/product/12614577/reviews?_shoppingMode=SITE&_regionCode=US&currencyCode=USD&_customerState=GUEST&_deviceType=DESKTOP&sort=NEWEST&limit=8
    pass


def save_prod(prod_list):
    pass


def save_comment(comment_list):
    pass


if __name__ == "__main__":
    url_ = "https://www.macys.com/shop/product/vince-camuto-off-the-shoulder-balloon-sleeve-top?ID=13164405&CategoryID=255"
    get_comment(url_)
