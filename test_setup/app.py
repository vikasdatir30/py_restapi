from flask import Flask
import pyodbc
import pandas as pd

app = Flask(__name__)


class Customer:
    def __init__(self):
        self.conn = pyodbc.connect('Driver={SQL Server};'
                                   'Server=VINIHOME-PC\SQLEXPRESS;'
                                   'Database=BikeStores;'
                                   'Trusted_Connection=yes;')

    def get_all_records(self):
        cursor = self.conn.cursor()
        try:
            data = cursor.execute('select top 10 customer_id,first_name,last_name,phone,email,'
                                  'street,city,state,zip_code from [sales].[customers]').fetchall()
            df = pd.DataFrame.from_records(data, columns=['customer_id', 'first_name', 'last_name', 'phone', 'email', 'street',
                                             'city', 'state', 'zip_code'])
            return df

        except Exception as e:
            print(e)
        finally:
            cursor.close()

    def get_customer_by_id(self, id):
        cursor = self.conn.cursor()
        try:
            data = cursor.execute(
                'select customer_id,first_name,last_name,phone,email,street,city,'
                'state,zip_code from [sales].[customers]'
                'where customer_id in ('+str(id)+')').fetchall()
            df = pd.DataFrame.from_records(data, columns=['customer_id', 'first_name', 'last_name', 'phone', 'email',
                                                          'street',
                                                          'city', 'state', 'zip_code'])
            return df

        except Exception as e:
            print(e)
        finally:
            cursor.close()


@app.route('/')
def index():
    return 'Hello to My REST API'


@app.route('/get')
def get_all():
    obj = Customer()
    df = obj.get_all_records()
    return df.to_json(orient='records')

@app.route('/get/<id>')
def get_by_id(id):
    obj = Customer()
    df = obj.get_customer_by_id(id)
    return df.to_json(orient='records')

