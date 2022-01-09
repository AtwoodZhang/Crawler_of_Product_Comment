url_rank2_normal_xpath = {'xpath_rank1': '//*[@id="row_1"]/ul/li/div/a',
                          'xpath_rank2_name': './picture/img/@alt',
                          'xpath_rank2_url': './@href'}
xpath_dict = {
    'url_rank1': {'//*[@id="mainNavigationFobs"]/li/a'},
    'url_rank2': {'Gifts & Toys': {'xpath_rank1': '//*[@id="bodyContainer"]/div/section[2]/div/div/div[2]/div/a',
                                   'xpath_rank2_name': './@id',
                                   'xpath_rank2_url': './@href'},
                  'Now Trending': {'xpath_rank1': '//*[@id="get-inspired"]/section/div/div/div/a',
                                   'xpath_rank2_name': './button/text()',
                                   'xpath_rank2_url': './@href'},
                  'Sale': {'xpath_rank1': '//*[@id="row_0"]/ul/li/div/div/a',
                           'xpath_rank2_name': './div/div/h3',
                           'xpath_rank2_url': './@href'},
                  'Women': url_rank2_normal_xpath,
                  'Men': url_rank2_normal_xpath,
                  'Kids & Baby': url_rank2_normal_xpath,
                  'Beauty': url_rank2_normal_xpath,
                  'Home': url_rank2_normal_xpath,
                  'Furniture ': url_rank2_normal_xpath,
                  'Shoes': url_rank2_normal_xpath,
                  'Jewelry': url_rank2_normal_xpath,
                  'Handbags & Accessories': url_rank2_normal_xpath},
    'url_rank3': {
        'product': '//*[@id="shop_all"]/div[2]/div/ul/li[2]/div/div[10]/ul/li/div/div/div/a',
        'product1': '//*[@id="shop_all"]/div[2]/div/ul/li[2]/div/div[10]/ul/li/div/div/div/div/a',
        'href': './@href',
        'cate_name': './@title',
        'next_page': "//*[@id='filterResultsBottom']/ul/li[2]/ul/li[@class='next-page']/div/a/@href",
    },
    'url_rank4': {'product_img',
                  'comment_page',
                  'comment_reviewer',
                  'comment_details',
                  }
}

re_dict = {
    'rank3': {
        'prod': '<div class="productDescription".*?a href="(.*?)" title="(.*?)" class="productDescLink".*?>',
        'next_page': '<div class="icon-ui-chevron-right-gr-huge".*?a href="(.*?)" aria-label=.*?Go forward to page.*?>'},

    'rank4': {
        'Web ID': '<p class="c-margin-bottom-4v web-id c-legal">Web ID:(.*?)</p>',
        'img': '<div class="media-wrapper image-grid-wrapper".*?class="main-picture">.*?<source type="image/webp" srcset="(.*?)">',
        'money': '<h3 class="tiered-prices h3 redesign-temp".*?div class="lowest-sale-price".*?span class=.*?>(.*?)</span>'}
}

# 产品评论规律查找
prod = {
    '''
    https://www.macys.com/shop/product/dkny-pleated-tie-neck-top?ID=7052689&CategoryID=255
    https://www.macys.com/xapi/digital/v1/product/7052689/reviews?_shoppingMode=SITE&_regionCode=US&currencyCode=USD&_customerState=GUEST&_deviceType=DESKTOP&sort=NEWEST&limit=30&offset=8
    https://www.macys.com/xapi/digital/v1/product/7052689/reviews?_shoppingMode=SITE&_regionCode=US&currencyCode=USD&_customerState=GUEST&_deviceType=DESKTOP&sort=NEWEST&limit=8
    
    https://www.macys.com/shop/product/dkny-pleated-tie-neck-top?ID=7052689&RVI=PDP_5&tdp=cm_choiceId~z7052689~xcm_pos~zPos5
    https://www.macys.com/xapi/digital/v1/product/7052689/reviews?_shoppingMode=SITE&_regionCode=US&currencyCode=USD&_customerState=GUEST&_deviceType=DESKTOP&sort=NEWEST&limit=30&offset=8
    https://www.macys.com/xapi/digital/v1/product/7052689/reviews?_shoppingMode=SITE&_regionCode=US&currencyCode=USD&_customerState=GUEST&_deviceType=DESKTOP&sort=NEWEST&limit=8
    
    https://www.macys.com/shop/product/style-co-sherpa-lined-zip-up-hoodie-created-for-macys?ID=12647912&CategoryID=255
    https://www.macys.com/xapi/digital/v1/product/12647912/reviews?_shoppingMode=SITE&_regionCode=US&currencyCode=USD&_customerState=GUEST&_deviceType=DESKTOP&sort=NEWEST&limit=30&offset=8
    https://www.macys.com/xapi/digital/v1/product/12647912/reviews?_shoppingMode=SITE&_regionCode=US&currencyCode=USD&_customerState=GUEST&_deviceType=DESKTOP&sort=NEWEST&limit=8
    
    https://www.macys.com/shop/product/dkny-printed-faux-wrap-top?ID=11835517&CategoryID=255&swatchColor=Black%2Fivory
    https://www.macys.com/xapi/digital/v1/product/11835517/reviews?_shoppingMode=SITE&_regionCode=US&currencyCode=USD&_customerState=GUEST&_deviceType=DESKTOP&sort=NEWEST&limit=8
    https://www.macys.com/xapi/digital/v1/product/11835517/reviews?_shoppingMode=SITE&_regionCode=US&currencyCode=USD&_customerState=GUEST&_deviceType=DESKTOP&sort=NEWEST&limit=30&offset=8
    
    
    https://www.macys.com/shop/product/calvin-klein-womens-faux-fur-trim-hooded-puffer-coat-created-for-macys?ID=12459475&CategoryID=269&swatchColor=Dark%20Chianti
    https://www.macys.com/xapi/digital/v1/product/12459475/reviews?_shoppingMode=SITE&_regionCode=US&currencyCode=USD&_customerState=GUEST&_deviceType=DESKTOP&sort=NEWEST&limit=8
    https://www.macys.com/xapi/digital/v1/product/12459475/reviews?_shoppingMode=SITE&_regionCode=US&currencyCode=USD&_customerState=GUEST&_deviceType=DESKTOP&sort=NEWEST&limit=30&offset=8
    https://www.macys.com/xapi/digital/v1/product/12459475/reviews?_shoppingMode=SITE&_regionCode=US&currencyCode=USD&_customerState=GUEST&_deviceType=DESKTOP&sort=NEWEST&limit=30&offset=38
    
    
    https://www.macys.com/shop/product/cole-haan-womens-box-quilt-down-puffer-coat?ID=2813247&CategoryID=269&swatchColor=Navy
    https://www.macys.com/xapi/digital/v1/product/2813247/reviews?_shoppingMode=SITE&_regionCode=US&currencyCode=USD&_customerState=GUEST&_deviceType=DESKTOP&sort=NEWEST&limit=8
    https://www.macys.com/xapi/digital/v1/product/2813247/reviews?_shoppingMode=SITE&_regionCode=US&currencyCode=USD&_customerState=GUEST&_deviceType=DESKTOP&sort=NEWEST&limit=30&offset=8
    https://www.macys.com/xapi/digital/v1/product/2813247/reviews?_shoppingMode=SITE&_regionCode=US&currencyCode=USD&_customerState=GUEST&_deviceType=DESKTOP&sort=NEWEST&limit=30&offset=38
    https://www.macys.com/xapi/digital/v1/product/2813247/reviews?_shoppingMode=SITE&_regionCode=US&currencyCode=USD&_customerState=GUEST&_deviceType=DESKTOP&sort=NEWEST&limit=30&offset=68
    https://www.macys.com/xapi/digital/v1/product/2813247/reviews?_shoppingMode=SITE&_regionCode=US&currencyCode=USD&_customerState=GUEST&_deviceType=DESKTOP&sort=NEWEST&limit=30&offset=98
    page20: 
    https://www.macys.com/xapi/digital/v1/product/2813247/reviews?_shoppingMode=SITE&_regionCode=US&currencyCode=USD&_customerState=GUEST&_deviceType=DESKTOP&sort=NEWEST&limit=30&offset=548
    '''

}
