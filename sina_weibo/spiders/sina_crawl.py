#coding=utf-8
import scrapy
import myconfig
import re
import json
from sina_weibo.items import SinaWeiboItem
from scrapy.shell import inspect_response

class DmozSpider(scrapy.spiders.Spider):
    name = "sina"
    allowed_domains = ["http://m.weibo.cn"]

    yunnanlvyou = 'http://m.weibo.cn/page/pageJson?containerid=&containerid=100103type%3D1%26q%3D%E4%BA%91%E5%8D%97%E6%97%85%E6%B8%B8&type=all&queryVal=%E4%BA%91%E5%8D%97%E6%97%85%E6%B8%B8&l_uicode=20000174&title=%E4%BA%91%E5%8D%97%E6%97%85%E6%B8%B8&featurecode=20000180&oid=3982714706748329&luicode=10000011&lfid=100103type%3D1%26q%3D%E4%BA%91%E5%8D%97%E6%97%85%E6%B8%B8&v_p=11&ext=&fid=100103type%3D1%26q%3D%E4%BA%91%E5%8D%97%E6%97%85%E6%B8%B8&uicode=10000011&next_cursor=&page='
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control":"max-age=0",
        "Connection": "keep-alive",
        "Host": "m.weibo.cn",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"
    }

    def start_requests(self):
        items = []
        i = 2
        while i<= 100:
            yield scrapy.Request(
                url=self.yunnanlvyou+str(i),
                headers=self.headers,
                # meta={
                #     'cookiejar': 1
                # },
                cookies={
                    '_T_WM': '750f353888c7a8cd3d35c940abf151f8',
                    'SUB': '_2A256U8OVDeTxGedJ6FcZ9CbJyD6IHXVZv-3drDV6PUJbkdBeLRbnkW0LozIgq7p3IB8VRxhFLZ1SbcfiKg..',
                    'SUHB': '0u5g08UJLT_Hus',
                    'SSOLoginState': '1465365446',
                    'M_WEIBOCN_PARAMS': 'uicode%3D20000174',
                    'gsid_CTandWM': '4udSCpOz5dzHwZjGBRVjf7hzy8A',
                },
                callback=self.search,
                dont_filter=True
            )
            i = i+1;

    def search(self, response):
        items = []

        # inspect_response(response, self)
        j = json.loads(response.body)
        index = 0

        while index<=8:


            text = j['cards'][0]['card_group'][index]['mblog']['text']
            text = re.sub('<.*?>', '', text)
            url = j['cards'][0]['card_group'][index]['scheme']
            date = j['cards'][0]['card_group'][index]['mblog']['created_at']
            author = j['cards'][0]['card_group'][4]['mblog']['user']['screen_name']
            item = SinaWeiboItem();
            item['content'] = text.encode('utf-8')
            item['url'] = url.encode('utf-8')
            item['date'] = date.encode('utf-8')
            item['author'] = author.encode('utf-8')
            items.append(item)
            index = index+1
        return items
