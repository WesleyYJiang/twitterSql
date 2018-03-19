import pymysql

db = pymysql.connect("localhost", "root", "j19y96t00", "Twitter")
cursor = db.cursor()

for i in range(100000):
    sql = "SELECT user_id FROM FOLLOWERS ORDER BY RAND() LIMIT 1"
    cursor.execute(sql)
    randomUser = cursor.fetchall()[0][0]
    sql = "SELECT * FROM TWEETS JOIN FOLLOWERS ON TWEETS.user_id = FOLLOWERS.follows_id  \
             WHERE FOLLOWERS.user_id = '%d' LIMIT 20" % (randomUser)
    cursor.execute(sql)

db.close()