from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app
from apps import app_geoviz, app_overview, app_plots

layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname'), ])
def display_page(pathname):
    if pathname == '/apps/overview':
        return app_overview.layout
    elif pathname == '/apps/geoviz':
        return app_geoviz.layout
    elif pathname == '/apps/plots':
        return app_plots.layout
    elif pathname == '/':
        return app_overview.layout
    else:
        return '404'
