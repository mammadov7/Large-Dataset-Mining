from app import app
from apps import app_root
import logging
logging.basicConfig(level=logging.INFO)

# The Webserver can either be run locally via the main function, or as a production level WSGI server (we use gunicorn)
# If it is executed as WSGI, no main function is executed, but instead the 'server' element is used directly.
# This means that we cannot put our initialization inside the main function.

app.logger.setLevel('INFO')
app.layout = app_root.layout  # We need to initialize the root layout before starting the webserver
server = app.server  # declare the server for gunicorn usage

if __name__ == '__main__':
    app.run_server(debug=True)  # This seems to run settings.py once more.
