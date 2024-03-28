import dash, logging, os
import dash_ag_grid as dag
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

domain_table = dag.AgGrid(
    id='domain-table',
    rowData = {},
    columnDefs=[{'headerName':'Domain Filter','field':'domain','filter':True, 
        'checkboxSelection': True,"resizable": False}],
    columnSize="sizeToFit",
    dashGridOptions={'rowSelection':'single'},
    className="ag-theme-alpine-dark"
)

fig = dcc.Graph(id = 'fig')

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
    Input('tabs','active_tab'),
    prevent_initial_call=True
)
def switch_tab(start_date, end_date, active_tab):
    start_date = date_to_epoch.convert(start_date)
    end_date = date_to_epoch.convert(end_date)
    domains = ftldns_worker.Worker().query_to_dataframe(f"""
        SELECT DISTINCT domain FROM queries WHERE timestamp BETWEEN {start_date} AND {end_date}  
    """)
    data = ftldns_worker.Worker().query_to_dataframe(f"""
        SELECT domain, timestamp, status  FROM queries WHERE timestamp BETWEEN {start_date} AND {end_date}  
    """)

    match active_tab:
        case 'frequency-tab':            
            domain_table.rowData = domains.to_dict("records")
            fig.figure = frequency_fig.generate(data)
            tab_content = html.Div([
                fig,
                html.Br(),
                dbc.Row([
                    dbc.Col(domain_table, width=3)
                ]) 
            ])
            return tab_content

        case 'entropy-tab':
            domain_table.rowData = domains.to_dict("records")
            fig.figure = entropy_fig.generate(data)
            tab_content = html.Div([
                fig,
                html.Br(),
                dbc.Row([
                    dbc.Col(domain_table, width=3)
                ]) 
            ])
            return tab_content
        
        case 'qot-tab':
            domain_table.rowData = domains.to_dict("records")
            fig.figure = qot_fig.generate(data)
            tab_content = html.Div([
                fig,
                html.Br(),
                dbc.Row([
                    dbc.Col(domain_table, width=3)
                ]) 
            ])
            return tab_content

@callback(
    Output('fig','figure'),
    State('tabs','active_tab'),
    Input('query-date-range', 'start_date'),
    Input('query-date-range', 'end_date'),
    Input('domain-table', 'selectedRows'),
    prevent_initial_call=True
)
def update_figure(active_tab,start_date,end_date,row):
    start_date = date_to_epoch.convert(start_date)
    end_date = date_to_epoch.convert(end_date)
    if row:
        domain_filter = row[0].get('domain')
        data = ftldns_worker.Worker().query_to_dataframe(f"""
            SELECT domain, timestamp, status  FROM queries WHERE timestamp BETWEEN {start_date} AND {end_date}
            AND domain = "{domain_filter}"
        """)
    else:
        data = ftldns_worker.Worker().query_to_dataframe(f"""
            SELECT domain, timestamp, status  FROM queries WHERE timestamp BETWEEN {start_date} AND {end_date}  
        """)
    match active_tab:
        case 'frequency-tab':            
            figure = frequency_fig.generate(data)
            return figure
        case 'entropy-tab':
            figure = entropy_fig.generate(data)
            return figure  
        case 'qot-tab':
            figure = qot_fig.generate(data)
            return figure

