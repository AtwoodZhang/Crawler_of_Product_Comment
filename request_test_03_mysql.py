# mysql language
import pymysql


class MysqlRank3(object):
    def __init__(self):
        self.db = pymysql.connect(
            host="localhost",  # 数据库服务端地址
            user='root',  # 链接数据库所使用的用户名
            passwd='root',  # 数据库密码
            db='macy',  # 数据库名称
            charset='utf8')
        # 创建游标对象
        self.cursor = self.db.cursor()

    def update_rank2_request_situation(self, cate_name, table_name='rank_2_url', situation='True'):
        sql = "update {0} set request_situation={1} where cate_name={2};".format(table_name, cate_name, situation)
        self.cursor.execute(sql)

    def select_rank2_urls(self, table_name, cate_name):
        sql = "select distinct {0} from {1} where request_situation <> 'True' or request_situation is NULL;" \
            .format(cate_name, table_name)
        self.cursor.execute(sql)

    def select_rank3_urls(self, table_name, cate_name):
        sql = "select distinct {0} from {1} where request_situation <> 'True' or request_situation is NULL;" \
            .format(cate_name, table_name)
        self.cursor.execute(sql)

    def select_rank2_all(self, table_name):
        sql = "select * from {} where request_situation <> 'True' or request_situation is NULL;".format(table_name)
        self.cursor.execute(sql)

    def insert_rank3_urls(self, table_name, cate_name1, cate_name2, cate_name1_value, cate_name2_value):
        sql = "insert into ({0} ({1}, {2}) values ({3},{4})"
        sql.format(table_name, cate_name1, cate_name2, cate_name1_value, cate_name2_value)
        self.cursor.execute(sql)

    def database_commit_close(self):
        self.cursor.close()
        self.db.close()
