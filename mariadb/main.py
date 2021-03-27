import pymysql

conn = None
cur = None

conn = pymysql.connect(host='',user='',password='',db='',charset='')
cur = conn.cursor()

sql = ''
cur.execute(sql)

conn.close()