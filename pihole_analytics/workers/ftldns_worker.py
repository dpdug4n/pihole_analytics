import sqlite3, logging
import pandas as pd

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Worker():
    def __init__(self):
        self.FTLDNS_PATH = "./pihole_analytics/pihole-FTL.db"
        self.query = "SELECT * FROM queries WHERE timestamp = null"
    def query_to_dataframe(self, query):
        try:
            logger.debug(f'Executing query: {query}')
            self.conn = sqlite3.connect(self.FTLDNS_PATH)
            self.df = pd.read_sql_query(query, self.conn)
            self.conn.close()  
            return self.df
        except sqlite3.Error as e:
            logger.error("Error querying data:", e)