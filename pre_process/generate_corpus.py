import pymysql.cursors

comments = 'comments.txt'
comment_ids = 'comment_ids.txt'


def is_valid(comment):
    if comment is not None and not comment == "":
        return True
    return False


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='shops',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
try:
    with connection.cursor() as cursor:
        sql = "SELECT `id`, `content` FROM `home_comment`"
        cursor.execute(sql)
        # debug
        with open(comments, 'w') as fc:
            with open(comment_ids, 'w') as fs:
                comment = ""
                shop_id = 0
                while True:
                    temp = cursor.fetchone()
                    if temp is not None and is_valid(temp['content']):
                        comment = temp['content'] + "\n"
                        fc.write(comment)
                        shop_id = str(temp['id']) + "\n"
                        fs.write(shop_id)
                    if temp is None:
                        break
finally:
    connection.close()