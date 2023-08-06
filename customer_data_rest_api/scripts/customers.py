import logging
import pandas as pd
from scripts.db_connector import DB_Connector


class Customers:
    def __init__(self, config):
        self.table_config = config['Database']
        self.db_connect = DB_Connector(config)

    def get_customer_by_id(self, id):
        try:
            sql_select = "select customer_id,first_name,last_name,phone,email,street,city,state,zip_code from "+\
                         self.table_config['db_table']+" where customer_id in (" + str(id) + ")"

            data = self.db_connect.get_data(sql_select)
            df = pd.DataFrame.from_records(data, columns=['customer_id', 'first_name', 'last_name', 'phone',
                                                          'email', 'street', 'city', 'state', 'zip_code'])
            return df
        except Exception as e:
            logging.error('Error in get_customer_by_id() : ', e)

    def get_n_customers(self, no_rows):
        try:
            sql_select = "select top " + str(
                no_rows) + "customer_id,first_name,last_name,phone,email,street,city,state,zip_code from "+self.table_config['db_table']
            data = self.db_connect.get_data(sql_select)
            df = pd.DataFrame.from_records(data, columns=['customer_id', 'first_name', 'last_name', 'phone',
                                                          'email', 'street', 'city', 'state', 'zip_code'])
            return df
        except Exception as e:
            logging.error('Error in get_n_customers() : ', e)


if __name__ == "__main__":
    Customers()
