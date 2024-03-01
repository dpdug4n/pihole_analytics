import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import dash_ag_grid as dag

from datetime import date

import workers.ftldns_worker as ftldns_worker 
import workers.date_to_epoch as date_to_epoch

## data
db_worker = ftldns_worker.Worker()
data = db_worker.query_to_dataframe(db_worker.query)
columnDefs = [{'field':col,'filter':True, 'sortable':True} for col in data.columns]

## UI
dash.register_page(
    __name__,
    name = "FTLDNS Browser",
    title = "FTLDNS Browser",
    description = "",
    location = "sidebar"                    
)

date_range = dcc.DatePickerRange(
    #https://dash.plotly.com/dash-core-components/datepickerrange
    id='query-date-range',
    start_date_placeholder_text="Start Period",
    end_date_placeholder_text="End Period",
    calendar_orientation='vertical',
    updatemode = 'bothdates',
    initial_visible_month = date.today(),
    min_date_allowed=date(1970,1,1), # change this to dynamically pull earliest date in FTLDNS
    max_date_allowed = date.today()
    # style = {'css_hell':'here'}
)

grid = dag.AgGrid(
    #https://dash.plotly.com/dash-ag-grid/getting-started
    id = "ftldns-browser",
    rowData=data.to_dict("records"),
    columnDefs=columnDefs,
    dashGridOptions={'pagination':True},#"domLayout":"autoHeight",
    # style = {}"
    className="ag-theme-alpine-dark"
)


def layout():
    return html.Div(
    [
        date_range,
        grid,
    ]
)

## callbacks
@callback(
    Output('ftldns-browser','rowData'),    
    Input('query-date-range', 'start_date'),
    Input('query-date-range', 'end_date')
)
def update_query_date_range(start_date, end_date):
    if start_date and end_date:
        start_date_epoch = date_to_epoch.convert(date.fromisoformat(start_date))
        end_date_epoch = date_to_epoch.convert(date.fromisoformat(end_date))
        query = f"SELECT * FROM queries WHERE timestamp BETWEEN {start_date_epoch} and {end_date_epoch}"
        data = db_worker.query_to_dataframe(query)
        return data.to_dict("records")
    