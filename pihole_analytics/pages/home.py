import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(
    __name__, 
    path='/',
    location = "sidebar"  
)

def layout():
    return dbc.Row(
        # [dbc.Col(sidebar(), width=2), dbc.Col(html.Div("Home"), width=10)]
    )