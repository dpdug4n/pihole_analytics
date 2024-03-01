import datetime 

def convert(date_obj):
    # Convert the date object to datetime object
    datetime_obj = datetime.datetime.combine(date_obj, datetime.time.min)
    
    # Get the epoch timestamp
    epoch_timestamp = int(datetime_obj.timestamp())
    
    return epoch_timestamp