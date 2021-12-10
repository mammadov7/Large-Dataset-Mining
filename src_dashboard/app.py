import dash

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
    # "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
    # "https://codepen.io/bcd/pen/KQrXdb.css",
    # "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
    # "https://codepen.io/dmcomfort/pen/JzdzEZ.css"
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
