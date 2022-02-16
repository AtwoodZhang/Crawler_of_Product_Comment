def normal_cope(case):  # man, woman等的爬取url方法；
    print(case, '-->  case_normal_cope')
    xpath_rank1 = '//*[@id="row_1"]/ul/li/div/a'
    xpath_rank2_name = './picture/img/@alt'
    xpath_rank2_url = './@href'
    xpath_list = [xpath_rank1, xpath_rank2_name, xpath_rank2_url]
    return xpath_list


def toy_and_gift(case):
    print(case, '-->  case_toy')
    xpath_rank1 = '//*[@id="bodyContainer"]/div/section[2]/div/div/div[2]/div/a'
    xpath_rank2_name = './@id'
    xpath_rank2_url = './@href'
    xpath_list = [xpath_rank1, xpath_rank2_name, xpath_rank2_url]
    return xpath_list


def trending(case):
    print(case, '-->  case_trending')
    xpath_rank1 = '//*[@id="get-inspired"]/section/div/div/div/a'
    xpath_rank2_name = './button/text()'
    xpath_rank2_url = './@href'
    xpath_list = [xpath_rank1, xpath_rank2_name, xpath_rank2_url]
    return xpath_list


def sale(case):
    print(case, '-->  case_sale')
    xpath_rank1 = '//*[@id="row_0"]/ul/li/div/div/a'
    xpath_rank2_name = './div/div/h3/text()'
    xpath_rank2_url = './@href'
    xpath_list = [xpath_rank1, xpath_rank2_name, xpath_rank2_url]
    return xpath_list


def furniture(case):
    print(case, '-->  case_furniture')
    xpath_rank1 = '//*[@id="row_3"]/ul/li/div/a'
    xpath_rank2_name = './div/picture/img/@alt'
    xpath_rank2_url = './@href'
    xpath_list = [xpath_rank1, xpath_rank2_name, xpath_rank2_url]
    return xpath_list


def home(case):
    print(case, '-->  case_home')
    xpath_rank1 = '//*[@id="row_2"]/ul/li/div/a'
    xpath_rank2_name = './picture/img/@alt'
    xpath_rank2_url = './@href'
    xpath_list = [xpath_rank1, xpath_rank2_name, xpath_rank2_url]
    return xpath_list


def handbags_and_accessories(case):
    print(case, '-->  case_handbags_and_accessories')
    xpath_rank1 = '//*[@id="row_1"]/ul/li/div/a'
    xpath_rank2_name = './picture/img/@alt'
    xpath_rank2_url = './@href'
    xpath_list = [xpath_rank1, xpath_rank2_name, xpath_rank2_url]
    return xpath_list


def kids_and_baby(case):
    print(case, '-->  case_kids_and_baby')
    xpath_rank1 = '//*[@id="row_0"]/ul/li/div/a'
    xpath_rank2_name = './picture/img/@alt'
    xpath_rank2_url = './@href'
    xpath_list = [xpath_rank1, xpath_rank2_name, xpath_rank2_url]
    return xpath_list


def gifts_and_toys(case):
    print(case, '-->  case_gifts_and_toys')
    xpath_rank1 = '//*[@id="giftsbyrecipient"]/div/div/div/div/div/div/div[2]/h5'
    xpath_rank2_name = './a/text()'
    xpath_rank2_url = './a/@href'
    xpath_list = [xpath_rank1, xpath_rank2_name, xpath_rank2_url]
    return xpath_list


def other(case):
    print('this case', case, 'is wrong!')


def get_xpath(mysql_data):
    dict_func = {
        'Gifts & Toys': gifts_and_toys,
        'Women': normal_cope,
        'Men': normal_cope,
        'Kids & Baby': kids_and_baby,
        'Beauty': normal_cope,
        'Home': home,
        'Furniture ': furniture,
        'Shoes': normal_cope,
        'Jewelry': normal_cope,
        'Handbags & Accessories': handbags_and_accessories,
        'Now Trending': trending,
        'Sale': sale
    }
    method = dict_func.get(mysql_data[1], other)
    if method:
        xpath_use = method(mysql_data[1])
        print(mysql_data[1])
        return xpath_use
    return False


def get_xpath_name2(mysql_data):
    dict_func = {
        'gifts & toys': gifts_and_toys,
        'women': normal_cope,
        'men': normal_cope,
        'kids & baby': kids_and_baby,
        'beauty': normal_cope,
        'home': home,
        'furniture': furniture,
        'shoes': normal_cope,
        'jewelry': normal_cope,
        'handbags & accessories': handbags_and_accessories,
        'now trending': trending,
        'sale': sale
    }
    method = dict_func.get(mysql_data[0], other)
    if method:
        xpath_use = method(mysql_data[0])
        # print(mysql_data[1])
        return xpath_use
    return False
