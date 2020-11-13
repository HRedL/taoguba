该网站的一些经验

1.cookies作为参数赋给Request，不要放在headers里面赋给Request

2.拼原贴的链接 new_topic_id + new_reply_id + “_1”

3.#访问主页,"https://www.taoguba.com.cn/blog/"+user_id

爬虫使用方法

1.stock里存储的是股票的相关“代码”，往这里面填对应的代码

2.登录一下淘股吧，更改下代码中的cookies

3.scrapy crawl taoguba（没安scrapy框架，需要安一下）







cookies需要单拿出来那玩意第一次见，改吐了