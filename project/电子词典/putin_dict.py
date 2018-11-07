import pymysql
import re


db = pymysql.connect(host = 'localhost', user = 'root', password = '123456', port = 3306, database = 'DICT', charset = 'utf8')
cursor = db.cursor()

with open('./dict.txt') as f:
    for line in f:
        print(line)
        try:
            d = re.match(r'(?P<WORD>[a-z]\S*)\s+(?P<ANNOTATION>.+)', line).groupdict()
        except:
            continue
        # print(d)
        cursor.execute('insert into words(word, interpret) value(%(WORD)s, %(ANNOTATION)s)', d)

    db.commit()
    cursor.close()
    db.close()


# f = open('./dict.txt')
# db = pymysql.connect('localhost', 'root', '123456', 'DICT')
# cursor = db.cursor()

# for line in f:
#     obj = re.match(r'([-a-zA-Z]+)\s+(.+)', line)
#     word = obj.group(1)
#     interpret = obj.group(2)

#     sql = 'insert into words(word, interpret) values(%s, %s)'%(word, interpret)

#     try:
#         cursor.execute(sql)
#         db.commit()
#     except:
#         db.rollback()

# f.close()
# cursor.close()
# db.close()