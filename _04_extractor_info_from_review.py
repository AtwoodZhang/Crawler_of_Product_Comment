import json
import pymysql
from _04_extractor_review_from_review import MyReviewInsert


def extractor_prod_info(review_path):
    review = open(review_path, "r", encoding="utf-8")
    review_data = json.load(review)
    info_dict = review_data['review']['includes']
    # print(info_dict)
    if info_dict is not None:
        info_dict = info_dict['products']
        # print("info_dict:", info_dict)
        print()
        for i in info_dict.items():
            print("i:", i)
            # print()
            info_dict = i[1]
            insert_worker = MyReviewInfoInsert(info_dict)
            review_dict = info_dict['reviewStatistics']
            if review_dict is not None:
                print("review_dict:", review_dict)
                insert_worker.insert_review_statistics(table_name="rank4_prod_specific_review_products"
                                                                  "rank4_prod_specific_review_products",
                                                       review=review_dict)
            else:
                insert_worker.insert_prod_description(table_name="rank4_prod_specific_review_products")
            insert_worker.database_commit_close()


class MyReviewInfoInsert(MyReviewInsert):
    def insert_prod_description(self, table_name):
        ND = self.one_review_dict
        sql1 = "insert ignore into {}".format(table_name)
        sql2 = "(description, imageUrl, name, productId, productPageUrl)"
        sql3 = "values"
        sql4 = "(\"{0}\", \"{1}\", \"{2}\", \"{3}\", \"{4}\")".format(ND["description"], ND["imageUrl"],
                                                                      ND["name"], ND["productId"],
                                                                      ND["productPageUrl"])
        sql = sql1 + sql2 + sql3 + sql4
        print(sql)
        self.cursor.execute(sql)
        self.db.commit()

    def insert_review_statistics(self, table_name, review):
        ND = review
        ND1 = self.one_review_dict
        # print("ND:", ND)
        # print("ND1:", ND1)
        sql1 = "insert ignore into rank4_prod_specific_review_products"
        sql2 = "(averageOverallRating, notRecommendedCount, overallRatingRange," \
               "ratingPercentage, ratingsOnlyReviewCount, recommendedCount, " \
               "totalReviewCount," \
               "description, imageUrl, name, productId, productPageUrl) "
        sql3 = "values "
        # print("1:", ND["averageOverallRating"])
        # print("2:", ND["notRecommendedCount"])
        # print("3:", ND["overallRatingRange"])
        # print("4:", ND["ratingPercentage"])
        # print("5:", ND["ratingsOnlyReviewCount"])
        # print("6:", ND["recommendedCount"])
        # print("7:", ND["totalReviewCount"])
        # print("8:", ND1["description"])
        # print("9:", ND1["imageUrl"])
        # print("10:", ND1["name"])
        # print("11:", ND1["productId"])
        # print("12:", ND1["productPageUrl"])
        sql4 = "({0}, {1}, {2}, {3}, {4}, {5}, " \
               "{6}, " \
               "\"{7}\", \"{8}\", \"{9}\", \"{10}\", " \
               "\"{11}\")".format(ND["averageOverallRating"],
                                  ND["notRecommendedCount"],
                                  ND["overallRatingRange"],
                                  ND["ratingPercentage"],
                                  ND["ratingsOnlyReviewCount"],
                                  ND["recommendedCount"],
                                  ND["totalReviewCount"],
                                  ND1["description"],
                                  ND1["imageUrl"],
                                  ND1["name"],
                                  ND1["productId"],
                                  ND1["productPageUrl"])
        sql = sql1 + sql2 + sql3 + sql4
        print("sql:", sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e)


"""
CREATE TABLE `macy`.`rank4_prod_specific_review_products` (
  `description` VARCHAR(500) NULL,
  `imageUrl` VARCHAR(500) NULL DEFAULT NULL,
  `name` VARCHAR(500) NULL DEFAULT NULL,
  `productId` VARCHAR(10) NOT NULL,
  `productPageUrl` VARCHAR(500) NULL DEFAULT NULL,
  `reviewStatistics` VARCHAR(5) NULL DEFAULT NULL,
  `averageOverallRating` FLOAT NULL DEFAULT NULL,
  `averageSliders` VARCHAR(45) NULL DEFAULT NULL,
  `notRecommendedCount` INT NULL DEFAULT NULL,
  `overallRatingRange` INT NULL DEFAULT NULL,
  `ratingDistribution` VARCHAR(5) NULL DEFAULT NULL,
  `ratingPercentage` INT NULL DEFAULT NULL,
  `ratingsOnlyReviewCount` INT NULL DEFAULT NULL,
  `recommendedCount` INT NULL DEFAULT NULL,
  `secondaryRatingsAverages` VARCHAR(45) NULL DEFAULT NULL,
  `secondaryRatingAveragesOrder` VARCHAR(45) NULL DEFAULT NULL,
  `totalReviewCount` INT NULL DEFAULT NULL,
  `locale` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`productId`));
"""