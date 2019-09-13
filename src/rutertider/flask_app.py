import flask

from rutertider import entur_api

DEFAULT_STOPID = "NSR:StopPlace:5968"
DEFAULT_QUAYS = ["NSR:Quay:10949"]
DEFAULT_LINE = "RUT:Line:3"


def _situation_generator(line_ids):
    """A generator that yields one situation at the time.

    This function loops over the provided line IDs and gets all relevant
    situation from Entur. It then yields one situation at the time.

    Args:
        line_ids: An iterable with line_id strings

    Returns:
        A generator

    Example:
        gen = _situation_generator([])
        situation = next(gen)
    """
    while True:
        situations = [sit.summary for line_id in line_ids for sit in
                      entur_api.get_situations(line_id)]
        if not situations:
            yield ''
        for sit in situations:
            yield sit


def create_app():
    app = flask.Flask(__name__)

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
        return flask.render_template("departure_table.html",
                                     departures=departures)

    @app.route('/deviations')
    def deviations():
        situations = _situation_generator(line_ids=[DEFAULT_LINE])
        return next(situations)

    return app
