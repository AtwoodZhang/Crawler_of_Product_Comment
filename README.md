# Crawler_of_Product_Comment
Macy's 

**Tips.** there is a little bit difference between the rank1's url's database and what I have written in the _01_main.py, so you have two choice about it.
1) copy and paste the url of "Women\ men \ toys and etc", and insert into the database.

or you can 

2) change database to the database what i have written in the code.

**environment:**
conda install requests

**run the code:**
1) unzip readme.zip
2) create a database the same as readme/爬取Macy网用户评价日志（1）需求存储数据库设计.docx
3) run the code: _01_main.py to download the url of rank1, like "Women、men、toys and etc"
4) run the code: _02_main.py  to download the url of rank2, like "Women --> tops 、 women --> hoddies、 and etc"
5) run the code: _03_main.py  to download the url of rank3, like "tops1, tops2 and etc"
6) run the code: _04_main.py  to download the url of rank4, is the true product's specific url.
7) run the code: _04_spider_of_rank4_prod_info_for_pic to download the img of prod.
8) run the code: _04_spider_of_rank4_prod_info_main.py to download the product information like price and name and etc.
9) run the code: _04_extractor_main.py to extract review information to database.
10) run the other code which has the code like: if __name__ == "__main__":

**Tips2:**
1) You'd better use the scrapy. scrapy is more robust than only use request like above codes.
