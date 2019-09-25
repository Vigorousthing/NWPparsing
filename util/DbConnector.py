import pymysql
import CONSTANT


class DbConnector:
    def __init__(self, site):
        if site == "jeju":
            host = CONSTANT.db_ip_jeju
        elif site == "nonsan":
            host = CONSTANT.db_ip_nonsan_gayagok1
        self.conn = pymysql.connect(host=host, user=CONSTANT.db_id, password=CONSTANT.db_pw, db=CONSTANT.db_name)

    def query(self, sql):
        curs = self.conn.cursor()
        curs.execute(sql)
        rows = curs.fetchall()
        self.conn.close()
        return rows