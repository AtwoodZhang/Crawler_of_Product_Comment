# Crawler_of_Product_Comment
Macy's 


1. Macy's 首先使用selenium进行尝试一；
    尝试一：
    from selenium.webdriver import Chrome
    # 1. 创建对象
    web = Chrome()
    # 2. 打开一个网址
    # web.get("https://www.macys.com/")
    # print(web.title)

    注释：Chrome提示正在收到自动测试软件的控制。
    Macy‘s的二级网址url无法进一步输入

    Macy's对Selenium的自动化控制进行了反扒。

    尝试二：
    去掉自动化控制提示，再进一步申请二级urls. 只是手动地去除了，但效果不是很行。

2.  用requests爬取第一页的产品url
    # 1. 进入1级url; 网页原始网址; 根据1级url,爬取所有man, woman, 等二级分类url;
         注意：1）这里使用了url_pool，有一定的随机性。url_pool中的headers有一定的随机性失效，得到permission deny;再运行两次就行；
              2）二级url存进rank_1_url表中；

    # 2. 根据2级url;遍历url,进入url所在网址；爬取所有3级url;如boots, sneakers等;各种小分类；
         注意：1）三级url通过二级url爬取，并存进rank_2_url表中；

        # Gifts & Toys
            # //*[@id="bodyContainer"]/div/section[2]/div/div/div[2]/div/a
            # ./@id                ---> names
            # ./@href              ---> url
        # woman
            # //*[@id="row_1"]/ul/li/div/a
            # ./@href              ---> url
            # ./picture/img/@alt   ---> names
        # man
            # //*[@id="row_1"]/ul/li/div/a
            # ./@href              ---> url
            # ./picture/img/@alt   ---> names
        # to Handbags& Accessories
        # Now Trending
            # //*[@id="get-inspired"]/section/div/div/div/a
            # ./@href              ---> url
            # ./button/text()      ---> names
        # Sale
            # //*[@id="row_0"]/ul/li/div/div/a
            # ./@href              ---> url
            # ./div/div/h3         ---> names

    # 3. 根据3级url;遍历url,进入url所在网址，爬取所有当页产品的所有url,然后点击下一页，到最后一页。爬取所有页面的所有产品的url;


    # 4. 根据4级url;遍历url,并进入具体url的页面，即具体产品的具体页面。然后可以尝试爬取具体产品的评论。
    # 5. 具体产品页需要爬取的对象：图片，页面，产品描述，等；

