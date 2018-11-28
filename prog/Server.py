import pymysql.cursors

# EXAMPLE
login = "sad"
password = "var"
try:
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 db='ibks',
                                 autocommit=True)
    with connection.cursor() as cursor:

        sql = "SELECT login FROM users WHERE login=%s" % (''.join(login))
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
        if result == None:
            sql = "INSERT INTO users (login, password) VALUES (%s, %s)" % (''.join(login), ''.join(password))
            cursor.execute(sql)
            print("good!")
        else:
            print("login is already exist!")
except pymysql.Error as e:
    connection.close()
