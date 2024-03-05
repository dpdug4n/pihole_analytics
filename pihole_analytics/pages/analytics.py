import dash
from dash import html
import dash_bootstrap_components as dbc

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

dash.register_page(
    __name__,
    name = "Analytics",  
    title = "Analytics",
    location = "sidebar"                 
)

def layout():
    return dbc.Row(
        # [dbc.Col(sidebar(), width=2), dbc.Col(html.Div("Analytics"), width=10)]
    )