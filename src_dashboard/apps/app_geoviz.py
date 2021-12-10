from dash import dcc
from dash import html
from dash.dependencies import Output, Input
from plotly import graph_objects as go

from app import app
from components.data import flight_df
from components.header import header
from utils.utils import subset_to_text, months_slider_ticks, carrier_dropdown_options, day_checklist_options, \
    days_of_week_num, delay_checklist_options, grouping_columns

subset = flight_df.copy()


# [{'label': 'Monday', 'value': 1}, {'label': 'Tuesday', 'value': 2}, ..., {'label': 'Sunday', 'value': 7}]


def create_map_figure(__subset):
    months = __subset.MONTH.unique()
    __subset = __subset.groupby(['DEPARTING_AIRPORT',]).sum().reset_index()
    count = __subset['COUNT']

    color = (100 * __subset['SUM_DEP_DEL15']) / count
    fig = go.Figure(data=go.Scattergeo(
        locationmode='USA-states',
        lon=__subset['LONGITUDE'] / count,
        lat=__subset['LATITUDE'] / count,
        text=subset_to_text(__subset, months=months),
        mode='markers',
        marker=dict(color=color,
                    # cmax=100,
                    cmin=0,
                    colorbar=dict(
                        title="Delayed <br>Flights (%)"
                    ),
                    colorscale='YlOrRd'),

    ))
    fig.update_layout(
        uirevision='constant',
        title='US Airports Flight Departures<br>(Hover for information)',
        geo=dict(
            scope='usa',
            projection_type='albers usa',
            showland=True,
            landcolor="rgb(0, 0, 0)",
            subunitcolor="rgb(100, 100, 100)",
            countrycolor="rgb(217, 217, 217)",
            countrywidth=0.5,
            subunitwidth=0.5,
        ),
    )

    return dcc.Graph(figure=fig),


layout = html.Div([
    header('Geoviz'),
    # html.H3('Overview'),
    html.Hr(),

    html.H5('Geographical visualisation'),
    html.Br(),
    # html.Button('Reset Cache', id='overview-reset-button'),
    html.Div([
        html.Div([
            html.Div(id='map-div'),
            dcc.RangeSlider(id='month-slider', min=1, max=12, step=1, marks=months_slider_ticks, value=[1, 12], )
        ], id='map-slider-div', style=dict(width='800px', display='inline-block', padding='5px',
                                           # border='3px solid red'
                                           )),
        html.Div([
            html.H6("Carrier"),
            dcc.Dropdown(id='carrier-dropdown',
                         options=carrier_dropdown_options,
                         placeholder='All Carriers',
                         style={'bottom': '5px'}  # dict(position='relative', top='10px', )
                         ),

            html.Div([
                html.Div([
                    html.H6("Day of Week"),
                    dcc.Checklist(id='day-checklist', options=day_checklist_options, value=days_of_week_num)
                ], id='days-div', style={'display': 'inline-block', 'height': '100%', },
                ),
                html.Div([
                    html.H6("Delays"),
                    dcc.Checklist(id='delay-checklist', options=delay_checklist_options, value=[0, 1])
                ], id='delay-div',
                    style={'display': 'inline-block', 'height': '100%', 'vertical-align': 'top', 'margin-left': '30px'},
                ),
            ], id='checklists-div')
        ],
            id='side-settings-div', style=dict(width='350px', height='100%')
        )

    ], id='geo-div', style={'display': 'flex', 'height': '100%',  # 'border': '3px solid green'
                            })

])


@app.callback(Output('map-div', 'children'),
              [Input('month-slider', 'value'), Input('carrier-dropdown', 'value'),
               Input('day-checklist', 'value'), Input('delay-checklist', 'value')])
def update_output(month_slider, carrier_name, days_chosen, delays_chosen):
    first_month, last_month = month_slider

    subset = flight_df.copy()

    first_month_idx = subset['MONTH'].apply(int) >= first_month
    last_month_idx = subset['MONTH'].apply(int) <= last_month
    day_idx = subset['DAY_OF_WEEK'].isin(days_chosen)

    delay_idx = subset['DEP_DEL15'].isin(delays_chosen)

    final_idx = first_month_idx & last_month_idx & day_idx & delay_idx

    if carrier_name:
        final_idx = final_idx & (subset['CARRIER_NAME'] == carrier_name)

    subset = subset[final_idx] #.groupby(grouping_columns)

    return create_map_figure(subset)[0]
