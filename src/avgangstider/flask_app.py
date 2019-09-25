import logging
from dataclasses import dataclass
from typing import List, Optional

import flask
from werkzeug.datastructures import ImmutableMultiDict

import avgangstider
from avgangstider.entur_api import Departure

# Module wide logger
LOG = logging.getLogger(__name__)
# LOG.setLevel(logging.DEBUG)


@dataclass
class AppArguments:
    """A container to hold request arguments"""
    stop_id: Optional[str]
    line_ids: List[str]
    platforms: List[str]
    max_queries: int
    max_departure_rows: int


def parse_args(args: ImmutableMultiDict
               ) -> AppArguments:
    """Parse the arguments received in the flask requests
    Args:
        An ImmutableMultiDict with the flask.request.args
    Returns:
         An AppData object with the corresponding data
    """
    # Extract arguments from the request
    stop_id = args.get('stop_id', type=str, default=None)
    platforms = args.getlist('platform', type=str)
    line_ids = args.getlist('line_id', type=str)
    max_queries = args.get('max_queries', type=int, default=10)
    max_departure_rows = args.get('max_rows', type=int, default=10)

    # Get rid of possible duplicates in lists
    line_ids = sorted(list(set(line_ids)))
    platforms = sorted(list(set(platforms)))

    app_data = AppArguments(
        stop_id=stop_id,
        platforms=platforms,
        line_ids=line_ids,
        max_queries=max_queries,
        max_departure_rows=max_departure_rows
    )
    LOG.debug("Created new AppData object, stop_id: {}, lines: {}".format(
        stop_id, line_ids))
    return app_data


def get_departures(app_data: AppArguments
                   ) -> List[Departure]:
    """Get a list of relevant departures from Entur
    Args:
        An AppData object with the requested arguments

    Returns:
        A list of Departures received from Entur
    """
    if app_data.stop_id is None:
        return []

    # Get new departure data
    departures = avgangstider.get_departures(
        stop_id=app_data.stop_id,
        platforms=app_data.platforms,
        line_ids=app_data.line_ids,
        max_departures=app_data.max_queries)
    # Don't return more than max_departure entries
    departures = departures[:app_data.max_departure_rows]
    LOG.debug("Got new departures for %s", app_data.stop_id)

    return departures


def create_app():
    app = flask.Flask(__name__)
    app.secret_key = b'\xb1\xf0\xe8\xe0%\x81\xe8\x93\x1b\xa6\xa7$\x0bu\xb9'

    @app.route('/')
    def departures_from_stop_id():
        # Parse received arguments
        stop_id = flask.request.args.get('stop_id', type=str, default=None)

        # If stop_id was not provided, redirect to help page
        if stop_id is None:
            return flask.redirect(flask.url_for('help_page'))

        # Get the request query
        request_query = flask.request.query_string.decode()
        query = flask.Markup(request_query)

        # If the current query is different than the old:
        # Reset the displayed_line_ids
        stored_query = flask.session.get('query', None)
        if query != stored_query:
            flask.session['query'] = query
            flask.session['displayed_line_ids'] = []

        # Otherwise, forward the query arguments to the other endpoints
        return flask.render_template("avgangstider.html", query=query)

    @app.route('/help')
    def help_page():
        return flask.render_template("help.html")

    @app.route('/departure_table')
    def departure_table():
        # Get latest departures and render template
        app_data = parse_args(flask.request.args)
        departures = get_departures(app_data)

        # What line_ids are we displaying?
        if app_data.line_ids:
            displayed_line_ids = set(app_data.line_ids)
        elif departures:
            displayed_line_ids = {
                departure.line_id for departure in departures
            }
        else:
            displayed_line_ids = set()

        # Store displayed line_ids in a client-side cookie
        current_displayed_ids = flask.session.get('displayed_line_ids', [])

        flask.session['displayed_line_ids'] = sorted(list(
            displayed_line_ids.union(current_displayed_ids)
        ))
        LOG.debug("Stored displayed lines: {}".format(
            flask.session['displayed_line_ids']))

        # Return template with departures
        return flask.render_template("departure_table.html",
                                     departures=departures)

    @app.route('/deviations')
    def deviations():
        # Get the currently displayed line_ids from clients cookie
        # We might have to wait until the get_departures has done it's job
        line_ids = flask.session.get('displayed_line_ids', None)
        LOG.debug("Situations: Got list from cookie: {}".format(line_ids))

        # Get current situations from Entur
        situations = [str(situation) for situation in
                      avgangstider.get_situations(line_ids)]

        # If there is nothing to display...
        if not situations:
            LOG.debug("No situations to display")
            return ''

        # Get the last displayed situation index from a client side cookie
        situation_idx = flask.session.get('last_situation', -1)

        # Increment situation index, wrap around and store it back
        situation_idx = (situation_idx + 1) % len(situations)
        flask.session['last_situation'] = situation_idx

        # Return next relevant situation
        return situations[situation_idx]

    return app


if __name__ == '__main__':
    # Start a Flask debugging server
    flask_app = create_app()
    LOG.setLevel(logging.DEBUG)
    flask_app.run(host='0.0.0.0', port=5000, debug=True)
