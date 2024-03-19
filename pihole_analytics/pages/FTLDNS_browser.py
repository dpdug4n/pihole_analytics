import dash, logging, os, asyncio
import dash_ag_grid as dag
from dash import html, dcc, Input, State, Output, ctx, callback
import dash_bootstrap_components as dbc

from datetime import date, timedelta


import pihole_analytics.workers.ftldns_worker as ftldns_worker 
import pihole_analytics.workers.date_to_epoch as date_to_epoch
import pihole_analytics.workers.result_normalizer as result_normalizer
import pihole_analytics.workers.domain_check as domain_check

# logging
log_level = logging.getLevelName(os.getenv('LOG_LEVEL'))
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

# data
db_worker = ftldns_worker.Worker()
data = db_worker.query_to_dataframe(db_worker.query)
data = result_normalizer.normalize(data)
columnDefs = [{'field':col,'filter':True, 'sortable':True} for col in data.columns]

# UI
dash.register_page(
    __name__,
    name = "FTLDNS Browser",
    title = "FTLDNS Browser",
    path = '/',
    description = "",
    location = "sidebar"                    
)

query_btn = dbc.Button(
    "Query All", 
    id="query-btn",
    color="primary"
)

count_btn = dbc.Button(
    "Count", 
    id="count-btn",
    color="primary"
)

check_btn = dbc.Button(
    "VT Lookup", 
    id="check-btn",
    color="secondary"
)

date_range = dcc.DatePickerRange(
    #https://dash.plotly.com/dash-core-components/datepickerrange
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

grid = dag.AgGrid(
    #https://dash.plotly.com/dash-ag-grid/getting-started
    id = "grid",
    rowData=data.to_dict("records"),
    columnDefs=columnDefs,
    dashGridOptions={'pagination':True, 'rowSelection':'single'},#"domLayout":"autoHeight",
    # style = {}"
    className="ag-theme-alpine-dark"
)

domain_results = html.Div(
    dcc.Markdown(
        id='domain-check-results',
        # classname = ''
        children = ''
    ),
    # style={}
)

def layout():
    return html.Div(
    [
        dbc.Row([
            dbc.Col(date_range, width="auto"),
            dbc.Col(query_btn, width="auto"),
            dbc.Col(count_btn,width="auto"),
            dbc.Col(check_btn,width="auto")
        ], justify="start"),
        grid,
        domain_results
    ]
)

#callbacks 

@callback(
    Output('grid','columnDefs'), 
    Output('grid','rowData'),  
    Input('query-btn','n_clicks'),  
    Input('count-btn','n_clicks'), 
    State('query-date-range', 'start_date'),
    State('query-date-range', 'end_date'),
    prevent_initial_call=True,
)
def update_query_date_range(qa_clicks,c_clicks, start_date, end_date):
    start_date_epoch = date_to_epoch.convert(start_date)
    end_date_epoch = date_to_epoch.convert(end_date)
    match ctx.triggered_id:
        case 'query-btn':
            query = f"""
                SELECT domain, type, status, timestamp, client, forward, additional_info, reply_type, reply_time, dnssec, id FROM queries 
                WHERE timestamp BETWEEN {start_date_epoch} and {end_date_epoch}
                """
        case 'count-btn':
            query = f"""
                SELECT domain, count(domain), type, status, client, forward, reply_type  FROM queries 
                WHERE timestamp BETWEEN {start_date_epoch} and {end_date_epoch} GROUP BY domain ORDER BY count(domain) DESC
                """
    data = ftldns_worker.Worker().query_to_dataframe(query)
    data = result_normalizer.normalize(data)
    columnDefs=[{'field':col,'filter':True, 'sortable':True, 'checkboxSelection': True} 
        if col == 'domain' else {'field':col,'filter':True, 'sortable':True} 
        for col in data.columns] 
        
    rowData = data.to_dict("records")
    return columnDefs, rowData

@callback(
    Output('check-btn','color'), 
    Input('grid','selectedRows'),  
    prevent_initial_call=True,
)
def check_btn_colorizer(row):
    if not row:
        return 'secondary'
    else:
        return 'primary'
    
@callback(
    Output('domain-check-results','children'), 
    State('grid','selectedRows'),  
    Input('check-btn','n_clicks'),
    prevent_initial_call=True,
)
def check_domain(row, clicks):
    if ctx.triggered_id == 'check-btn':
        result = domain_check.domain_lookup(row[0].get('domain'))
        # logger.debug(result)
        return result