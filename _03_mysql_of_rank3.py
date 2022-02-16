import pymysql


class MacyRank3Mysql(object):
    def __init__(self):
        self.db = pymysql.connect(
            host="localhost",  # 数据库服务端地址
            user='root',  # 链接数据库所使用的用户名
            passwd='root',  # 数据库密码
            db='macy',  # 数据库名称
            charset='utf8')
        # 创建游标对象
        self.cursor = self.db.cursor()

    def select_upper_no_request(self, table_name):
        sql = "select * from {0} where request_situation <> 'True' or request_situation is NULL;".format(table_name)
        self.cursor.execute(sql)
        # 2. 显示取出的表数据的结构
        col_name_list = [a[0] for a in self.cursor.description]
        print("mysql category: ", col_name_list)

    def database_commit_close(self):
        self.cursor.close()
        self.db.close()