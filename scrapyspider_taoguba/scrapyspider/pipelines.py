
import pymysql
from scrapyspider.items import Review
from scrapy import log


class ScrapyspiderPipeline(object):


    def process_item(self, item, spider):

       # 连接数据库
        my_sql = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', charset='utf8',
                                 db='taoguba', use_unicode=True)
        # 获取游标
        cur = my_sql.cursor()
        try:
            if isinstance(item, Review):
                cur.execute("INSERT INTO review(content,user_name,subject,action_date,user_id,new_reply_id,new_topic_id,zan_num,stock_attr,view_num,total_fans_num,sid) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            [item['content'],item['userName'],item['subject'],item['actionDate'],item['userId'],item['newReplyId'],item['newTopicId'],
                             item['zanNum'],item['stockAttr'],item['viewNum'],item['totalFansNum'],item['sid']])

                # 提交
                my_sql.commit()
                # 关闭游标
                cur.close()
                # 关闭数据库连接
                my_sql.close()
        except Exception as e:
            log.msg("写入数据库出现异常33333333333333333333333333333333333333333333333333333333333333333", level=log.WARING)
            my_sql.commit()
            cur.close()
            my_sql.close()
        finally:
            return item
