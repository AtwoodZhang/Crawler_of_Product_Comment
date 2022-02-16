'''
# I ignore the create tables language

# add the first page urls
use macy;
insert into rank1_cate_urls(cate_name, cate_url) values
("sale","https://www.macys.com/shop/sale?id=3536&cm_sp=us_hdr-_-sale-_-3536_sale"),
("women", "https://www.macys.com/shop/womens-clothing?id=118&cm_sp=us_hdr-_-women-_-118_women"),
("men", "https://www.macys.com/shop/mens-clothing?id=1&cm_sp=us_hdr-_-men-_-1_men"),
("kids & baby", "https://www.macys.com/shop/kids-clothes?id=5991&cm_sp=us_hdr-_-kids-%26-baby-_-5991_kids-%26-baby"),
("beauty", "https://www.macys.com/shop/makeup-and-perfume?id=669&cm_sp=us_hdr-_-beauty-_-669_beauty"),
("home", "https://www.macys.com/shop/for-the-home?id=22672&cm_sp=us_hdr-_-home-_-22672_home"),
("furniture", "https://www.macys.com/shop/furniture?id=29391&cm_sp=us_hdr-_-furniture--_-29391_furniture-"),
("shoes", "https://www.macys.com/shop/shoes?id=13247&cm_sp=us_hdr-_-shoes-_-13247_shoes"),
("jewelry", "https://www.macys.com/shop/jewelry-watches?id=544&cm_sp=us_hdr-_-jewelry-_-544_jewelry"),
("handbags & accessories","https://www.macys.com/shop/handbags-accessories?id=26846&cm_sp=us_hdr-_-handbags-%26-accessories-_-26846_handbags-%26-accessories"),
("now trending", "https://www.macys.com/shop/contemporary-nocrawl?id=315556&cm_sp=us_hdr-_-now-trending-_-315556_now-trending"),
("gifts & toys", "https://www.macys.com/shop/gift-guide?id=118142&cm_sp=us_hdr-_-gifts-%26-toys-_-118142_gifts-%26-toys");


# create prod info
CREATE TABLE `macy`.`rank4_prod_specific_info1` (
  `web_id` VARCHAR(10) NOT NULL,
  `prod_name` VARCHAR(100) NULL DEFAULT NULL,
  `prod_url` VARCHAR(500) NOT NULL,
  `prod_before_price` FLOAT NULL DEFAULT NULL,
  `prod_now_price` FLOAT NOT NULL,
  PRIMARY KEY (`web_id`),
  UNIQUE INDEX `web_id_UNIQUE` (`web_id` ASC) VISIBLE,
  UNIQUE INDEX `prod_url_UNIQUE` (`prod_url` ASC) VISIBLE);


'''