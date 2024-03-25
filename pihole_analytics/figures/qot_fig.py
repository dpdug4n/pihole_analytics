import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os, logging

import pihole_analytics.workers.result_formatter as result_formatter
# logging
log_level = logging.getLevelName(os.getenv('LOG_LEVEL'))
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

def generate(data):
    try:
        data = result_formatter.format(data)
        floor_to_hour = lambda x: x.replace(minute=0, second=0, microsecond=0)
        data.timestamp = data.timestamp.apply(floor_to_hour)
        data_grouped = data.groupby(['timestamp', 'domain','status']).size().reset_index(name='count')
        color_mapping = {
            "Unknown: Unknown status (not yet known)":"grey",
            "Allowed: Replied from stale cache": "green",
            "Allowed: Forwarded":"green",
            "Allowed: Replied from cache":"green",
            "Allowed: Retried query":"green",
            "Allowed: Retried but ignored query (this may happen during ongoing DNSSEC validation)":"green",
            "Allowed: Already forwarded, not forwarding again":"green",
            "Blocked: Domain contained in gravity database":"red",
            "Blocked: Domain matched by a regex blacklist filter":"red",
            "Blocked: Domain contained in exact blacklist":"red",
            "Blocked: By upstream server (known blocking page IP address)":"red",
            "Blocked: By upstream server (0.0.0.0 or ::)":"red",
            "Blocked: By upstream server (NXDOMAIN with RA bit unset)":"red",
            "Blocked:Domain contained in gravity database.":"red",
            "Blocked: Domain matched by a regex blacklist filter.":"red",
            "Blocked: Domain contained in exact blacklist":"red",
            "Blocked: Blocked (database is busy)":"red",
            "Blocked: Blocked (special domain)":"red",

        }

        fig = px.bar(data_grouped,
            title='Doman Queries Over Time',
            x='timestamp', 
            y='count', 
            color='status',
            barmode='stack',
            labels={'count': 'Domain Count', 'timestamp':'Date'},
            hover_data={'timestamp': '|%B %d, %Y %H:00', 'domain': True, 'status': True, 'count': True},
            color_discrete_map=color_mapping,
            template='plotly_dark')
        return fig
    
    except Exception as error:
        logger.error(type(error).__name__)
        logger.error(error)