import flask
from . import entur_api

app = flask.Flask(__name__)


@app.route('/')
def create_ruter_departures():
    request_query = flask.request.query_string.decode()
    return flask.render_template("rutertider.html", query=flask.Markup(request_query))


@app.route('/departure_table')
def departure_table():
    stopid = str(flask.request.args.get('stopid', default=entur_api.DEFAULT_STOPID,
                                        type=str))
    platforms = flask.request.args.getlist('platforms', type=str)
    lines = flask.request.args.getlist('lines', type=str)
    max_rows = flask.request.args.get('rows', type=int)
    departures = entur_api.get_departures(stopid=stopid, platforms=platforms,
                                          lines=lines, max_rows=max_rows)
    return flask.render_template("departure_table.html", departures=departures)


@app.route('/deviations')
def deviations():
    situations = entur_api.get_situations(line=entur_api.DEFAULT_LINE)
    return situations[0]
