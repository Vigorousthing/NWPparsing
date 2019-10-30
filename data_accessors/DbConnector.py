import pymysql
import CONSTANT
import pandas as pd


class NuriDbConnector:
    def __init__(self):
        self.conn = None
        self.curs = None

    def query(self, sql):
        self.curs.execute(sql)
        self.conn.close()
        return self.curs.fetchall()

    @staticmethod
    def dataframe_converter(*args):
        result = []
        for i in args:
            result.append(pd.DataFrame(i))

        result = result[0].append(result[1])
        return result


class JejuDbConnector(NuriDbConnector):
    def __init__(self):
        super(JejuDbConnector, self).__init__()
        self.conn = pymysql.connect(host=CONSTANT.db_ip_jeju,
                                    user=CONSTANT.db_id,
                                    password=CONSTANT.db_pw,
                                    db="rtu",
                                    cursorclass=pymysql.cursors.DictCursor)
        self.curs = self.conn.cursor()


class NonsanDbConnector(NuriDbConnector):
    def __init__(self):
        super(NonsanDbConnector, self).__init__()
        self.conn_gayagok = pymysql.connect(
            host=CONSTANT.db_ip_nonsan_gayagok1, user=CONSTANT.db_id,
            password=CONSTANT.db_pw, db="rtu",
            cursorclass=pymysql.cursors.DictCursor)
        self.conn_yujin = pymysql.connect(
            host=CONSTANT.db_ip_nonsan_gayagok1, user=CONSTANT.db_id,
            password=CONSTANT.db_pw, db="rtu",
            cursorclass=pymysql.cursors.DictCursor)
        self.curs_gayagok = self.conn_gayagok.cursor()
        self.curs_yujin = self.conn_yujin.cursor()

    def query(self, sql):
        self.curs_gayagok.execute(sql)
        self.conn_gayagok.close()
        result1 = self.curs_gayagok.fetchall()

        self.curs_yujin.execute(sql)
        self.conn_yujin.close()
        result2 = self.curs_yujin.fetchall()

        return self.dataframe_converter(result1, result2)

        # return self.curs_gayagok.fetchall(), self.curs_yujin.fetchall()

jenon_sql = "select tbl_inverter_min.recvdate - INTERVAL 10 MINUTE, " \
      "sum(tbl_inverter_min.KWD) " \
      "from tbl_inverter_min " \
      "WHERE tbl_inverter_min.recvdate " \
      "BETWEEN '{}' AND '{}' " \
      "GROUP BY MONTH(tbl_inverter_min.recvdate), " \
      "DAY(tbl_inverter_min.recvdate), " \
      "HOUR(tbl_inverter_min.recvdate - INTERVAL 10 MINUTE)  " \
      "ORDER BY tbl_inverter_min.recvdate"


if __name__ == '__main__':

    start_time = "2019-01-01"
    end_time = "2019-10-02"

    sql = "select tbl_inverter_min.recvdate - INTERVAL 10 MINUTE, " \
          "sum(tbl_inverter_min.KWD) " \
          "from tbl_inverter_min INNER JOIN " \
          "tbl_kma_min ON tbl_inverter_min.recvdate = tbl_kma_min.recvdate  " \
          "WHERE tbl_inverter_min.recvdate " \
          "BETWEEN '{}' AND '{}' " \
          "GROUP BY MONTH(tbl_inverter_min.recvdate), " \
          "DAY(tbl_inverter_min.recvdate), " \
          "HOUR(tbl_inverter_min.recvdate - INTERVAL 10 MINUTE)  " \
          "ORDER BY tbl_inverter_min.recvdate"
    con = NonsanDbConnector().query(sql.format(start_time, end_time))
    print(con)

    import pandas as pd
    a = pd.DataFrame(con)

