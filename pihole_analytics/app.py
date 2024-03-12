import dash, logging, os
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dotenv import load_dotenv

# config/env
load_dotenv()

# logging
log_level = logging.getLevelName(os.getenv('LOG_LEVEL'))
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

app = Dash(__name__, use_pages=True,external_stylesheets=[dbc.themes.DARKLY])

server = app.server

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "primary",
}
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

app.layout = html.Div([
    html.Div([
        html.H2("PiHole Analytics", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    html.Div(page["name"], className="navbar-dark"),
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values() if page["location"] == "sidebar"
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE
    ),
    html.Div(
        dash.page_container,
        style=CONTENT_STYLE
    )
])

if __name__ == '__main__':
    app.run(debug=True, port=8686)