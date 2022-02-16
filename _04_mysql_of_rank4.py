from _03_mysql_of_rank3 import MacyRank3Mysql
import re


def filter_web_id_from_rank3_table():
    web_id_bug = MacyRank4Mysql()
    web_id_bug.select_url_from_rank3_table()
    one_mysql_data = web_id_bug.cursor.fetchone()
    web_id_result = []

    while one_mysql_data is not None:
        # step1. 取一条
        web_string = one_mysql_data[0]
        re_string = "https:.*?\?ID=(.*?)&.*?"
        string_pattern = re.compile(re_string, re.S)
        result = string_pattern.findall(web_string)
        # print("ID:", result)

        # step2. 插入web_id至rank4_prod_info
        web_id_insert_bug = MacyRank4Mysql()

        # step2.1 插入web_id
        # web_id_insert_bug.insert_web_id(table_name="rank4_prod_specific_info", cate_name="prod_id", id_num=result[0])
        # web_id_insert_bug.database_commit_close()
        # step2.2 查看web_id, 并插入url.
        # web_id_insert_bug.update_web_url_has_id(table_name="rank4_prod_specific_info",
        #                                         cate_name="prod_url",
        #                                         web_url=web_string,
        #                                         has_cate_name="prod_id",
        #                                         has_id_num=result[0])
        # step2.3 同时插入web_id和url
        web_id_insert_bug.insert_web_id(table_name="rank4_prod_specific_info", cate_name="prod_id,prod_url",
                                        id_num="{0}', '{1}".format(result[0], web_string))

        # step3. 取下一条
        one_mysql_data = web_id_bug.cursor.fetchone()
        web_id_result.append(result[0])

    web_id_bug.database_commit_close()
    print("web_id's length:", len(web_id_result))


class MacyRank4Mysql(MacyRank3Mysql):
    def select_upper_no_request(self, table_name):
        sql = "select * from {0} where request_situation <> 'True' or request_situation is NULL;".format(table_name)
        self.cursor.execute(sql)
        # 2. 显示取出的表数据的结构
        col_name_list = [a[0] for a in self.cursor.description]
        print("mysql category: ", col_name_list)

    def select_info_no_request_url4(self, table_name, cate_name):
        sql = "select * from {0} where {1} is NULL and page_web_id is NULL;".format(table_name, cate_name)
        # sql = "select * from {0} where {1} is NULL;".format(table_name, cate_name)
        self.cursor.execute(sql)
        # 2. 显示取出的表数据的结构
        col_name_list = [a[0] for a in self.cursor.description]
        print("mysql category: ", col_name_list)

    def select_url_from_rank3_table(self):
        sql = "select cate_url from rank3_cate_urls;"
        self.cursor.execute(sql)
        # 2. 显示取出的表数据的结构
        col_name_list = [a[0] for a in self.cursor.description]
        print("mysql category: ", col_name_list)

    def insert_web_id(self, table_name, cate_name, id_num):
        sql = "insert ignore into {0}({1}) values('{2}')".format(table_name, cate_name, id_num)
        print(sql)
        self.cursor.execute(sql)
        self.db.commit()

    def update_web_url_has_id(self, table_name, cate_name, has_cate_name, web_url, has_id_num):
        sql = "update {0} set {1}='{2}' where {3}='{4}'"\
            .format(table_name, cate_name, web_url, has_cate_name, has_id_num)
        print(sql)
        self.cursor.execute(sql)
        self.db.commit()

    def update_rank4_request_situation(self, table_name, prod_id):
        sql = "update {0} set request_situation='True' where prod_id='{1}';".format(table_name, prod_id)
        print(sql)
        self.cursor.execute(sql)
        self.db.commit()

    def select_unrequest_prod_img(self, table_name):
        sql = "select * from {0} where img_request_situation <> 'True' or img_request_situation is NULL;"\
            .format(table_name)
        print(sql)
        self.cursor.execute(sql)
        # 2. 显示取出的表数据的结构
        col_name_list = [a[0] for a in self.cursor.description]
        print("mysql category: ", col_name_list)


if __name__ == "__main__":
    filter_web_id_from_rank3_table()
