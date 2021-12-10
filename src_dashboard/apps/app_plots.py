import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
from plotly import graph_objects as go

from app import app
from components.data import flight_df
from components.header import header
from utils.utils import months_slider_ticks, day_checklist_options, days_of_week_num, \
    delay_checklist_options, airport_dropdown_options, months

subset = flight_df.copy()

layout = html.Div([
    header('Plots'),
    # html.H3('Overview'),
    html.Hr(),

    html.H5('Hierarchical Visualisation'),
    html.Br(),
    # html.Button('Reset Cache', id='overview-reset-button'),
    html.Div([
        html.Div([
            html.Div(id='sunburst-div'),
            dcc.RangeSlider(id='month-slider', min=1, max=12, step=1, marks=months_slider_ticks, value=[1, 12], )
        ], id='map-slider-div', style=dict(width='800px', display='inline-block', padding='5px',
                                           # border='3px solid red'
                                           )),
        html.Div([
            html.H6("Airport"),
            dcc.Dropdown(id='airport-dropdown',
                         options=airport_dropdown_options,
                         placeholder='All Airports',
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
        ),

    ], id='plots-div', style={'display': 'flex', 'height': '100%',  # 'border': '3px solid green'
                              }),
    html.Div(id='barchart-div', style={'width': '1000px'}),

])


def create_bar_chart(__subset):
    fig = go.Figure(
        data=[
            go.Bar(name='Summed Delays', x=__subset['MONTH_NAME'], y=__subset['SUM_DEP_DEL15'], yaxis='y', offsetgroup=1),
            go.Bar(name='Ratio of Delays', x=__subset['MONTH_NAME'], y=__subset['PCT_DEP_DEL15'], yaxis='y2', offsetgroup=2)
        ],
        layout={
            'title': 'Flight Delays over 15 Minutes ',
            'yaxis': {'title': 'Number of Delays'},
            'yaxis2': {'title': 'Percentage of Delays (%)', 'overlaying': 'y', 'side': 'right'}
        }
    )

    fig.update_layout(
        xaxis_tickfont_size=14,
        yaxis=dict(
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1  # gap between bars of the same location coordinate.
    )

    return dcc.Graph(figure=fig)


@app.callback(Output('sunburst-div', 'children'),
              Output('barchart-div', 'children'),
              [Input('month-slider', 'value'), Input('airport-dropdown', 'value'),
               Input('day-checklist', 'value'), Input('delay-checklist', 'value')])
def update_output(month_slider, airport_name, days_chosen, delays_chosen):
    first_month, last_month = month_slider

    subset = flight_df.copy()

    first_month_idx = subset['MONTH'].apply(int) >= first_month
    last_month_idx = subset['MONTH'].apply(int) <= last_month
    day_idx = subset['DAY_OF_WEEK'].isin(days_chosen)

    delay_idx = subset['DEP_DEL15'].isin(delays_chosen)

    final_idx = first_month_idx & last_month_idx & day_idx & delay_idx

    if airport_name:
        final_idx = final_idx & (subset['DEPARTING_AIRPORT'] == airport_name)

    subset = subset[final_idx]
    subset['SNOWY'] = subset.SNOW.apply(lambda x: 'Snow' if x > .1 else 'No Snow')
    subset['MONTH_NAME'] = subset['MONTH'].map(months_slider_ticks)

    if len(subset) > 0:
        sunburst_fig = px.sunburst(subset, path=['CARRIER_NAME', 'MONTH_NAME', 'SNOWY', ], values='DEP_DEL15', maxdepth=2)
    else:
        sunburst_fig = px.sunburst()

    subset_months = months[first_month - 1:last_month]
    subset_months = [m for m in subset_months if m in subset['MONTH_NAME'].unique()]

    bar_group = subset[['MONTH_NAME', 'SUM_DEP_DEL15', 'COUNT']].groupby('MONTH_NAME').sum().loc[
        subset_months].reset_index()
    bar_group['PCT_DEP_DEL15'] = 100. * bar_group['SUM_DEP_DEL15'] / bar_group['COUNT']

    return dcc.Graph(figure=sunburst_fig), create_bar_chart(bar_group)
