from dash import dcc
from dash import html


def header(active_element: str = None):
    return html.Div([
        get_logo(),
        # get_header(),
        html.Br(),
        get_menu(active_element)
    ])


def get_logo():
    logo = html.Div([

        html.Div([
            html.Img(src='../assets/telecom_logo.png', height='120', style={'float': 'right'})
        ]),

        html.Div([
            html.H2('Flight Delay Dataset', style={'float': 'left'})
        ])

    ], className="row gs-header")
    return logo


def get_header():
    header_value = html.Div([
        html.Div([
            html.H5('Flight Visualisation', style={'float': 'left'})
        ])

    ])
    return header_value


def get_menu(active_element: str):
    menu = html.Div([
        dcc.Link('Overview', href='/apps/overview', className="tab", style=get_style(active_element, 'Overview')),
        dcc.Link('Departure Maps', href='/apps/geoviz', className="tab", style=get_style(active_element, 'Geoviz')),
        dcc.Link('Plots', href='/apps/plots', className="tab", style=get_style(active_element, 'Plots')),
    ], className="row")
    return menu


def get_style(active_element: str, menu_element: str):
    base_style = {"padding": "5px", "color": "black"}

    if active_element == menu_element:
        active_style = base_style.copy()
        active_style.update({"font-weight": "bold", "color": "black"})
        return active_style
    else:
        return base_style
