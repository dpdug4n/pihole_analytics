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
            "Allowed: Replied from stale cache": "#008000",
            "Allowed: Forwarded":"#00CC00",
            "Allowed: Replied from cache":"#008000",
            "Allowed: Retried query":"#33FF33",
            "Allowed: Retried but ignored query (this may happen during ongoing DNSSEC validation)":"#33FF33",
            "Allowed: Already forwarded, not forwarding again":"#008000",
            "Blocked: Domain contained in gravity database":"#FF3333",
            "Blocked: Domain matched by a regex blacklist filter":"#FF3333",
            "Blocked: Domain contained in exact blacklist":"#FF3333",
            "Blocked: By upstream server (known blocking page IP address)":"#CC0000",
            "Blocked: By upstream server (0.0.0.0 or ::)":"#CC0000",
            "Blocked: By upstream server (NXDOMAIN with RA bit unset)":"#CC0000",
            "Blocked: Blocked (database is busy)":"#800000",
            "Blocked: Blocked (special domain)":"#800000",
        }

        fig = px.bar(data_grouped,
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