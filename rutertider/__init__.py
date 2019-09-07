import flask
from . import entur_api

app = flask.Flask(__name__)

DEFAULT_STOPID = "NSR:StopPlace:5968"
DEFAULT_QUAYS = ["NSR:Quay:10949"]
DEFAULT_LINE = "RUT:Line:3"


@app.route('/')
def create_ruter_departures():
    request_query = flask.request.query_string.decode()
    return flask.render_template("rutertider.html",
                                 query=flask.Markup(request_query))


@app.route('/departure_table')
def departure_table():
    # Extract arguments from the request
    stop_id = flask.request.args.get('stop_id', type=str,
                                     default=DEFAULT_STOPID)
    platforms = flask.request.args.getlist('platforms', type=str)
    lines = flask.request.args.getlist('lines', type=str)
    max_departures = flask.request.args.get('max_departures', type=int,
                                            default=10)

    # Create a list of relevant departures
    departures = entur_api.get_departures(stop_id=stop_id,
                                          platforms=platforms,
                                          lines=lines,
                                          max_departures=max_departures)
    return flask.render_template("departure_table.html", departures=departures)


def _deviations(line):
    situations = entur_api.get_situations(line)
    while situations:
        for sit in situations:
            yield sit
    else:
        yield ''


@app.route('/deviations')
def deviations():
    situations = _deviations(line=DEFAULT_LINE)
    return next(situations)
