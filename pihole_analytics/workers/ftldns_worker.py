import sqlite3, logging, os
import pandas as pd

# logging
log_level = logging.getLevelName(os.getenv('LOG_LEVEL'))
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

class Worker():
    def __init__(self):
        self.FTLDNS_PATH = "./pihole_analytics/pihole-FTL.db"
        self.query = """
            SELECT domain, type, status, timestamp, client, forward, additional_info, reply_type, reply_time, dnssec, id 
            FROM queries WHERE timestamp = null
            """
    def query_to_dataframe(self, query):
        try:
            logger.debug(f'Executing query: {query}')
            self.conn = sqlite3.connect(self.FTLDNS_PATH)
            self.df = pd.read_sql_query(query, self.conn)
            self.conn.close()  
            logger.debug(f"Query Results:\n{self.df}")
            return self.df
        except sqlite3.Error as e:
            logger.error("Error querying data:", e)