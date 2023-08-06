import sys
import tomli
import os
import logging
from datetime import datetime as dt
from scripts.customers import Customers

from flask import Flask

rest_app = Flask(__name__)

# set datetime for logs
run_datetime = dt.now().strftime('%Y-%m-%d_%H_%M')

# getting current path and parent folder name for future use
CURRENT_DIR = os.getcwd()
PARENT_DIR = os.path.dirname(CURRENT_DIR)

# set global variable for future request
config = None

# function to read config file
def get_config(file_path):
    file_path = CURRENT_DIR + "/" + file_path
    print(file_path)
    try:
        if os.path.isfile(file_path):
            with open(file_path, mode='rb') as cnf_file:
                config = tomli.load(cnf_file)
                return config
        else:
            raise Exception('Config file not found')
    except Exception as e:
        print("Error in get_config():", e)


@rest_app.route("/")
def home():
    docs_str = """ <html> <body>
    <h3><b><u>Welcome to Customer Data REST API</h3></b></u><br>
    Use following pattern in URL to get customer data <br>
    1. /get_by_id/cust_id : To get a customer record by ID ex: http://127.0.0.1:8560/get/123 <br>
    2. /get_n_rows/n_rows  : To get n number of rows from customer table ex: http://127.0.0.1:8560/get/500 <br>
    </body></html>
    """
    return docs_str


@rest_app.route("/get_by_id/<cust_id>")
def get_by_id(cust_id):
    cust_obj = Customers(config)
    df = cust_obj.get_customer_by_id(cust_id)
    return df.to_json(orient='records')


@rest_app.route("/get_n_rows/<n_rows>")
def get_by_n_rows(n_rows):
    cust_obj = Customers(config)
    df = cust_obj.get_n_customers(n_rows)
    return df.to_json(orient='records')


def main_caller():
    global config
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = sys.argv[2]
        config_file_path = sys.argv[3]
        config = get_config(config_file_path)

        # setting log config
        log_file = CURRENT_DIR + '/' + config['Logger']['log_prefix'] + str(run_datetime) + '.log'
        logging.basicConfig(level=logging.DEBUG,
                            format="%(asctime)s [%(levelname)s]: %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S",
                            handlers=[logging.StreamHandler(), logging.FileHandler(log_file)])

        # string rest api
        rest_app.run(host=host, port=port)
    else:
        print('Wrong no of arguments')


if __name__ == "__main__":
    main_caller()
