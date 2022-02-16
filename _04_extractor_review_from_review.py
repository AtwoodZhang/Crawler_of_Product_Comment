import json
import pymysql


def extractor_review(review_path):
    review = open(review_path, "r", encoding="utf-8")
    review_data = json.load(review)
    review_list = review_data['review']['reviews']
    print(len(review_list))
    if len(review_list) > 0:
        for i in review_list:
            print(i)
            insert_worker = MyReviewInsert(i)
            insert_worker.insert_prod_id(table_name="rank4_prod_specific_review_reviews")
            insert_worker.database_commit_close()


class MyReviewInsert(object):
    def __init__(self, one_review_dict):
        super(MyReviewInsert, self).__init__()
        self.one_review_dict = one_review_dict
        self.db = pymysql.connect(
            host="localhost",  # 数据库服务端地址
            user='root',  # 链接数据库所使用的用户名
            passwd='root',  # 数据库密码
            db='macy',  # 数据库名称
            charset='utf8')
        # 创建游标对象
        self.cursor = self.db.cursor()

    def insert_prod_id(self, table_name):
        ND = self.one_review_dict
        sql1 = "insert ignore into {}".format(table_name)
        sql2 = "(anonymous, authorId, productId, " \
               "displayName, reviewId, reviewText, " \
               "lastModificationTime, submissionTime, " \
               "rating, ratingPercentage, ratingRange, ratingsOnly, reviewerId, " \
               "topContributor, totalFeedbackCount, totalNegativeFeedbackCount, totalPositiveFeedbackCount," \
               "userNickname)"
        sql3 = "values(\"{0}\", \"{1}\", \"{2}\", " \
               "\"{3}\", \"{4}\", \"{5}\", " \
               "\"{6}\", \"{7}\", " \
               "{8}, {9}, {10}, \"{11}\", \"{12}\", " \
               "\"{13}\", {14}, {15}, {16}, " \
               "\"{17}\")".format(ND["anonymous"], ND["authorId"], ND["productId"],
                                  ND["displayName"], ND["reviewId"], ND["reviewText"],
                                  ND["lastModificationTime"], ND["submissionTime"],
                                  ND["rating"], ND["ratingPercentage"], ND["ratingRange"], ND["ratingsOnly"],
                                  ND["reviewerId"],
                                  ND["topContributor"], ND["totalFeedbackCount"], ND["totalNegativeFeedbackCount"],
                                  ND["totalPositiveFeedbackCount"],
                                  ND["userNickname"])
        sql = sql1+sql2+sql3
        print(sql)
        self.cursor.execute(sql)
        self.db.commit()

    def database_commit_close(self):
        self.cursor.close()
        self.db.close()