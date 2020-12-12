import sqlite3 as sql





def save_to_db(dataframe):
    conn = sql.connect('weather.db')
    dataframe.to_sql('weather', conn)