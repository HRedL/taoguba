import scrapy
import pymysql
from bs4 import BeautifulSoup
from scrapyspider.items import Review
import time
import json


# 继承自scrapy.Spider
class TripadvisorSpider(scrapy.Spider):

    name = "taoguba"

    def start_requests(self):

        cookies = "UM_distinctid=1759d19823116a-04c6d15b3a51a6-67e1b3f-e1000-1759d19823220d; __gads=ID=46659d0bd89c11c7-22950e4b91c40086:T=1604658601:RT=1604658601:S=ALNI_MZOGonpm9x9k2m9y7zMeSGYEVVbLA; tgbuser=5383541; tgbpwd=73D654585B7pd5q4opl7kcr0gc; onedayyszc=1604678400000; CNZZDATA1574657=cnzz_eid%3D789273175-1604654960-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1605268471; JSESSIONID=cd6ff23d-3c1f-4a4b-9601-08ded6a34b12; Hm_lvt_cc6a63a887a7d811c92b7cc41c441837=1604659998,1605233283,1605272439,1605272459; Hm_lpvt_cc6a63a887a7d811c92b7cc41c441837=1605272538"
        cookies = {i.split('=')[0]: i.split('=')[1] for i in cookies.split('; ')}

        my_sql = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', charset='utf8',
                                 db='taoguba', use_unicode=True)
        cur = my_sql.cursor()
        cur.execute("SELECT id,code FROM stock")

        datas = cur.fetchall()
        for data in datas:
            sid, code = data
            url = f"https://www.taoguba.com.cn/quotes/getStockAccurate?stockCode={code}&actionDate=&perPageNum=20&isOpen=false"

            yield scrapy.Request(url=url, cookies=cookies,
                                 callback=lambda response,sid=sid, code=code: self.parse(response, sid,code))




    def parse(self,response, sid, code):


        cookies = "UM_distinctid=1759d19823116a-04c6d15b3a51a6-67e1b3f-e1000-1759d19823220d; __gads=ID=46659d0bd89c11c7-22950e4b91c40086:T=1604658601:RT=1604658601:S=ALNI_MZOGonpm9x9k2m9y7zMeSGYEVVbLA; tgbuser=5383541; tgbpwd=73D654585B7pd5q4opl7kcr0gc; onedayyszc=1604678400000; CNZZDATA1574657=cnzz_eid%3D789273175-1604654960-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1605268471; JSESSIONID=cd6ff23d-3c1f-4a4b-9601-08ded6a34b12; Hm_lvt_cc6a63a887a7d811c92b7cc41c441837=1604659998,1605233283,1605272439,1605272459; Hm_lpvt_cc6a63a887a7d811c92b7cc41c441837=1605272538"
        cookies = {i.split('=')[0]: i.split('=')[1] for i in cookies.split('; ')}

        jsonBody = json.loads(response.text.encode('utf-8'))

        datas = jsonBody['dto']['record']
        for data in datas:
            review = Review()
            review['content'] = data['body']
            review['userName'] = data['userName']
            review['subject'] = data['subject']
            review['actionDate'] = data['actionDate']

            # 访问主页,id
            review['userId'] = data['userID']
            # 拼原贴的链接 new_topic_id + new_reply_id
            review['newReplyId'] = data['newReplyID']
            review['newTopicId'] = data['newTopicID']
            review['zanNum'] = data['usefulNum']
            review['viewNum'] = data['viewNum']
            review['totalFansNum'] = data['totalFansNum']
            review['sid'] = sid
            stock_attr = data['stockAttr']
            if len(stock_attr) > 0:
                review['stockAttr'] = ','.join([d['stockCode'] for d in stock_attr])
            else:
                review['stockAttr'] = ''
            yield review
        if "actionDate" in jsonBody['dto'].keys():
            actionDate = jsonBody['dto']['actionDate']
            url = f"https://www.taoguba.com.cn/quotes/getStockAccurate?stockCode={code}&actionDate={actionDate}&perPageNum=20&isOpen=false"
            yield scrapy.Request(url=url, cookies=cookies,
                                 callback=lambda response, sid=sid, code=code: self.parse(response,sid, code))



