import sqlite3
import pandas as pd

class Worker():
    def __init__(self):
        self.FTLDNS_PATH = "/etc/pihole/pihole-FTL.db" #change this to pull from ENV var
        self.query = "SELECT * FROM queries WHERE timestamp = null"
    def query_to_dataframe(self, query):
        try:
            self.conn = sqlite3.connect(self.FTLDNS_PATH)
            self.df = pd.read_sql_query(query, self.conn)
            self.conn.close()
            return self.df
        except sqlite3.Error as e:
            print("Error querying data:", e)