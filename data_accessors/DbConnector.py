import pymysql
import CONSTANT


class DbConnector:
    def __init__(self, site):
        self.conn = None
        self.curs = None

        if site == "jeju":
            self.conn = pymysql.connect(host=CONSTANT.db_ip_jeju,
                                        user=CONSTANT.db_id,
                                        password=CONSTANT.db_pw,
                                        db="rtu")
            self.curs = self.conn.cursor()
        elif site == "nonsan":
            self.conn = pymysql.connect(host=CONSTANT.db_ip_nonsan_gayagok1,
                                        user=CONSTANT.db_id,
                                        password=CONSTANT.db_pw,
                                        db="rtu")
            self.curs = self.conn.cursor()

    def query(self, sql):
        self.curs.execute(sql)
        self.conn.close()
        return self.curs.fetchall()

