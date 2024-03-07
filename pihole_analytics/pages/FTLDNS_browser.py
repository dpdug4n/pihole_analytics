import dash, logging, json
import dash_ag_grid as dag
from dash import html, dcc, Input, State, Output, ctx, callback
import dash_bootstrap_components as dbc

from datetime import date, timedelta

import pihole_analytics.workers.ftldns_worker as ftldns_worker 
import pihole_analytics.workers.date_to_epoch as date_to_epoch
import pihole_analytics.workers.result_normalizer as result_normalizer

# logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# data
db_worker = ftldns_worker.Worker()
data = db_worker.query_to_dataframe(db_worker.query)
data = result_normalizer.normalize(data)
columnDefs = [{'field':col,'filter':True, 'sortable':True} for col in data.columns]

## UI
dash.register_page(
    __name__,
    name = "FTLDNS Browser",
    title = "FTLDNS Browser",
    description = "",
    location = "sidebar"                    
)

query_btn = dbc.Button(
    "Update", 
    id="query-btn",
    color="primary"
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
    dashGridOptions={'pagination':True},#"domLayout":"autoHeight",
    # style = {}"
    className="ag-theme-alpine-dark"
)

def layout():
    return html.Div(
    [
        dbc.Row([
            dbc.Col(date_range, width="auto"),
            dbc.Col(query_btn, width="auto")
        ], justify="start"),
        grid
    ]
)
@callback(
    Output('grid','columnDefs'), 
    Output('grid','rowData'),  
    Input('query-btn','n_clicks'),  
    State('query-date-range', 'start_date'),
    State('query-date-range', 'end_date'),
    prevent_initial_call=True,
)
def update_query_date_range(n_clicks,start_date, end_date):
    if ctx.triggered_id == 'query-btn' and n_clicks !=0 :
        start_date_epoch = date_to_epoch.convert(start_date)
        end_date_epoch = date_to_epoch.convert(end_date)
        query = f"SELECT * FROM queries WHERE timestamp BETWEEN {start_date_epoch} and {end_date_epoch}"
        data = ftldns_worker.Worker().query_to_dataframe(query)
        data = result_normalizer.normalize(data)
        columnDefs=[{'field':col,'filter':True, 'sortable':True} for col in data.columns]
        rowData = data.to_dict("records")
        return columnDefs, rowData
