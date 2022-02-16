import os
from concurrent.futures import ThreadPoolExecutor  # 用来构建线程池
from _04_extractor_info_from_review import extractor_prod_info
from _04_extractor_review_from_review import extractor_review
from _00_record_of_small_functions import *
import time


txt_path = "D:\\zya\\Crawler_of_Product_Comment\\crawler_of_Macy_version1.0\\prod_review"  # 待读取的文件夹


def run():
    # step1. 拿到路径下文件名
    global txt_path
    path_txt_list = os.listdir(txt_path)
    path_txt_list.sort()
    print("filename example: ", path_txt_list[0])
    print("coping file count:", len(path_txt_list))

    # test
    # path_txt_list = path_txt_list[0:2]

    # step2. 将文件名提交给数据库插入任务
    with ThreadPoolExecutor(1) as t:
        for i in path_txt_list:
            t.submit(extract_review, i)


def extract_review(txt_name):
    global txt_path
    json_path = os.path.join(txt_path, txt_name)

    # step3. 提取数据并插入数据库；
    # extractor_review(json_path)
    extractor_prod_info(json_path)


if __name__ == "__main__":
    # step1. 写入日志
    log_path = './prod_crawl_log/'
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_file_name = log_path + 'log-' + time.strftime("%Y%m%d-%H%M%S", time.localtime()) + 'review_txt_to_base' + '.log'
    sys.stdout = Logger(log_file_name)
    sys.stderr = Logger(log_file_name)

    # step2. 运行替换过程；
    run()
