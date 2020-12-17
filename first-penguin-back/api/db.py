import pymysql
import random

conn = pymysql.connect(host='ttobak.cbbaovh5sf1x.ap-northeast-2.rds.amazonaws.com',user='root',password='soma2020',db='ttobak',charset='utf8')

curs = conn.cursor()

sql = """insert into stu_cure(cure_txt,date,cure_id,stu_id,ori_answer,stu_answer,is_review,is_daily,is_first,is_correct) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

dates = ['2020-11-14','2020-11-15','2020-11-16','2020-11-17','2020-11-18','2020-11-19']

for d in dates:
    for i in range(10):
        ori_answer = random.randint(1,3)
        stu_answer = random.randint(1,3)
        is_correct = 'F'
        if ori_answer == stu_answer:
            is_correct = 'T'
            

        curs.execute(sql,('count',d,1898,85,ori_answer,stu_answer,'F','F','F',is_correct))
    
conn.commit()

conn.close()
