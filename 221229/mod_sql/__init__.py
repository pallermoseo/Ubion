# 모듈의 목적은? 
import pymysql
import pandas as pd

class Database():
    def __init__(self, _host, _user, _pass):
        self._db = pymysql.connect(
            host = _host,
            user = _user,
            password = _pass,
            port = 3306,
            db = 'ubion'
        )
        self.cursor = self._db.cursor(pymysql.cursors.DictCursor)
    
    # select 쿼리문을 실행하는 경우 사용하는 함수
    def executeAll(self, _sql, _values = [], _limit = 0):
        self.cursor.execute(_sql, _values)
        self.result = self.cursor.fetchall()
        if _limit != 0:
            self.df = pd.DataFrame(self.result).head(_limit)
        else:
            self.df = pd.DataFrame(self.result)
        
        return self.df

    # select 문을 제외한 데이터베이스의 내용을 삽입, 수정, 삭제하는 경우
    def execute(self, _sql, _values = []):
        self.cursor.execute(_sql, _values)
        self.result = self.cursor.fetchall()
        return self.result

    def commit(self):
        self._db.commit()
        return 'commit complete'

    # 모든 작업 종료 후 데이터베이스와의 접속을 종료
    def close(self):
        self._db.close()
        return 'Database Close'
