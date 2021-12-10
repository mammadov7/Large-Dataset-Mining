from dash import html

from components.header import header

layout = html.Div([
    header('Overview'),
    html.Hr(),

    html.P('Welcome to our visualisation dashboard for SD201 Mining of Large Datasets'),
    html.Br(),
    html.P([html.B('Please be aware of the following:')]),
    html.Ol([
        html.Li('You can find a map of airports with flight information in "Departure Maps".'),
        html.Li('You can find a hierarchical sunburst chart and a bar chart information in "Plots".'),
        html.Li('As the plots are recreated dynamically, there may be some latency.'),
    ]),

    html.Div(id='overview-hidden-div', style={'display': 'none'}),
])

