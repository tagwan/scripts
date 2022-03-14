import pymysql


class ReadMysql(object):
    db_name = "conquerlogin"
    sql_query = "select * from cluster_info;"

    def __init__(self, url, username, passwd) -> None:
        self.url = url
        self.username = username
        self.passwd = passwd

    def run(self) -> None:
        """
        run
        :return:
        """
        # 打开数据库连接
        db = pymysql.connect(self.url, self.username, self.passwd, self.db_name)

        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        # 使用 execute()  方法执行 SQL 查询
        cursor.execute(self.sql_query)

        # 使用 fetchone() 方法获取单条数据.
        data = cursor.fetchone()

        print(type(data))
        print(data)

        self.dispose(db)

    @staticmethod
    def dispose(db) -> None:
        # 关闭数据库连接
        db.close()


if __name__ == '__main__':
    url = "localhost"
    user = "root"
    password = "123456"
    ReadMysql(url, user, password).run()
