from datetime import datetime 
import logging 

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def convert(date_str):
    logger.debug(f'Converting {date_str} to epoch.')
    date_object = datetime.strptime(date_str, "%Y-%m-%d")
    epoch_timestamp = int(date_object.timestamp())
    return epoch_timestamp