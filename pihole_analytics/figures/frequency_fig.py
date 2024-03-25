import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os, logging

# logging
log_level = logging.getLevelName(os.getenv('LOG_LEVEL'))
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

# Work in progress
def generate(data):
    try:
        logger.debug('Generating frequency fig')
        fig = px.line(template='plotly_dark')
        return fig
    
    except Exception as error:
        logger.error(type(error).__name__)
        logger.error(error)