import pyodbc
import logging as log


class DB_Connector:
    def __init__(self, config):
        self.db_config = config['Database']
        try:
            self.connect = pyodbc.connect('Driver={'+self.db_config['db_driver']+'};'
                                          'Server='+self.db_config['db_server']+';'
                                          'Database='+self.db_config['db_database']+';'
                                          'Trusted_Connection=yes;')
        except Exception as e:
            log.error("Error in __init__()", e)

    def get_data(self, query):
        cursor = self.connect.cursor()
        try:
            data = cursor.execute(query).fetchall()
            return data
        except Exception as e:
            log.error("Error in  get_data() : ", e)
        finally:
            cursor.close()