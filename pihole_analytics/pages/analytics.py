import dash, logging, os
from dash import html, dcc, Input, State, Output, ctx, callback
import dash_bootstrap_components as dbc

from datetime import date, timedelta

import pihole_analytics.workers.ftldns_worker as ftldns_worker 
import pihole_analytics.workers.date_to_epoch as date_to_epoch
import pihole_analytics.figures.entropy_fig as entropy_fig
import pihole_analytics.figures.frequency_fig as frequency_fig
import pihole_analytics.figures.qot_fig as qot_fig

# logging
log_level = logging.getLevelName(os.getenv('LOG_LEVEL'))
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

# ui
dash.register_page(
    __name__,
    name = "Analytics",  
    title = "Analytics",
    location = "sidebar"                 
)
date_range = dcc.DatePickerRange(
    id='query-date-range',
    start_date_placeholder_text="Start Period",
    start_date=date.today() - timedelta(weeks=1),
    end_date=date.today(),
    calendar_orientation='vertical',
    initial_visible_month = date.today(),
    min_date_allowed=date(1970,1,1), # change this to dynamically pull earliest date in FTLDNS?
    max_date_allowed = date.today(),
    updatemode="bothdates",
    # style = {'css_hell':'here'}
)

tabs = dbc.Tabs(
    [
        dbc.Tab(label='Frequency',tab_id='frequency-tab',
            active_tab_class_name = "nav-item nav-link active bg-dark",     
        ),
        dbc.Tab(label='Entropy',tab_id='entropy-tab',
            active_tab_class_name = "nav-item nav-link active bg-dark",      
        ),
        dbc.Tab(label='Queries over Time',tab_id='qot-tab',
            active_tab_class_name = "nav-item nav-link active bg-dark",      
        ),
    ],
    id = "tabs"
)

def layout():
    return html.Div([
        dbc.Row([
            dbc.Col(tabs),
            dbc.Col(date_range, width = "auto")
        ]),
        html.Div(id='tab-content')
    ])


# callbacks
@callback(
    Output('tab-content', 'children'),
    Input('query-date-range', 'start_date'),
    Input('query-date-range', 'end_date'),
    Input("tabs","active_tab"),
    prevent_initial_call=True
)
def switch_tab(start_date, end_date, active_tab,):
    start_date = date_to_epoch.convert(start_date)
    end_date = date_to_epoch.convert(end_date)
    data = ftldns_worker.Worker().query_to_dataframe(f"""
        SELECT domain, timestamp, status  FROM queries WHERE timestamp BETWEEN {start_date} AND {end_date}  
    """)
    match active_tab:
        case 'frequency-tab':
            # domains = ftldns_worker.Worker().query_to_dataframe(
            #     "SELECT DISTINCT domain FROM queries")['domain'].tolist()
            # domain_dropdown = dbc.DropdownMenu(id="domain-dropdown",
            #     menu_variant="dark",
            #     label="Domains",
            #     children = [ 
            #         dbc.DropdownMenuItem(f"{domain}",id = f"{domain}-btn")        
            #         for domain in domains
            #     ],
            #     style = {"max-height":"400px"}                             
            # )
            
            tab_content = html.Div([
                dcc.Graph(
                    id = 'frequency-fig',
                    figure = frequency_fig.generate(data)
                )
            ])
            return tab_content

        case 'entropy-tab':
            tab_content = html.Div([
                dcc.Graph(
                    id = 'entropy-fig',
                    figure = entropy_fig.generate(data)
                )
            ])
            return tab_content
        
        case 'qot-tab':
            tab_content = html.Div([
                dcc.Graph(
                    id = 'qot-fig',
                    figure = qot_fig.generate(data)
                )
            ])
            return tab_content