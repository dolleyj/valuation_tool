import json
import pandas as pd
import sqlite3 as sql

# to edit an existing entry in the sql with pandas.to_sql: if_exists='replace'


def convert_dict_to_dataframe(dic):
    print(dic)
    # return pd.DataFrame.from_dict(dic)
    return pd.DataFrame.from_dict([dic])
    # return pd.DataFrame(dic)


def get_all_stocks():
    conn = sql.connect('data/valuation_tool.db')

    # Read stocks into a dataframe
    df = pd.read_sql_query("SELECT * FROM stocks;", conn)

    #Drop the index column TODO: Doesnt seem to work :/ 
    df.drop(axis=1, columns=['index'])
    print(df)

    return json.loads(df.to_json(orient='records'))


# TODO - Delete a stock from the stocks table
def remove_stock_from_db(stock):
    pass



def save_to_db(stock_data):
    success = False

    # Convert dict to pandas dataframe
    df = convert_dict_to_dataframe(stock_data)
    print(df)

    try:
        conn = sql.connect('data/valuation_tool.db')
        df.to_sql('stocks', conn, if_exists='append')
        success = True

    except Error as e:
        print("Unable to save stock data to database: \n")
        print(e)

    return success