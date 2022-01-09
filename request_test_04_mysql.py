from request_test_03_mysql import MysqlRank3

create_review_table = ''
'''
   CREATE TABLE review(
        anonymous VARCHAR(10),
        authorId VARCHAR(20),
        badges VARCHAR(50),
        badgesOrder VARCHAR(10),
        clientResponses VARCHAR(50),
        contentLocale VARCHAR(50),
        contextDataValues VARCHAR(50),
        contextDataValuesOrder VARCHAR(50),
        displayName VARCHAR(50),
        featured VARCHAR(10),
        incentivizedReview VARCHAR(10),
        lastModificationTime VARCHAR(50),
        moderationStatus VARCHAR(50),
        photos VARCHAR(2083),
        productId VARCHAR(20) FOREIGN KEY REFERENCES prod(WebID)
        rating INT,
        ratingPercentage INT,
        ratingRange INT,
        ratingsOnly VARCHAR(50),
        reviewId VARCHAR(50) PRIMARY KEY,
        reviewText VARCHAR(2083),
        reviewerId VARCHAR(50),
        secondaryRatings VARCHAR(50),
        submissionTime VARCHAR(100),
        syndicated VARCHAR(50),
        title VARCHAR(1000),
        topContributor VARCHAR(50),
        totalFeedbackCount INT,
        totalNegativeFeedbackCount INT,
        totalPositiveFeedbackCount INT,
        userNickname VARCHAR(50),        
        videos VARCHAR(2083),
        );
'''
create_prod_table = ''
'''
create table prod(
    WebId VARCHAR(20) PRIMARY KEY,
    imageUrl VARCHAR(2083),
    Prod_Id VARCHAR(50),
    ProductPageUrl VARCHAR(2083),
    Description VARCHAR(2083),
    Before_Price FLOAT,
    Now_Price FLOAT NOT NULL,
    Request_situation VARCHAR(10)
);
'''


class MysqlRank4(MysqlRank3):
    def new_prod_message_insert(self, web_id, image_url, prod_page_url,
                                before_price, now_price, request_situation='False'):
        sql = "insert into (WebId, imageUrl, ProductPageUrl,Before_Price, Now_Price, Request_situation) " \
              "VALUES('{0}', '{1}', '{2}', {3}, {4}, '{5}')"
        sql.format(web_id, image_url, prod_page_url, before_price, now_price, request_situation)
        self.cursor.execute(sql)
