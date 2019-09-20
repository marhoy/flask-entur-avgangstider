import logging
import time

import flask

import rutertider

# Module wide logger
LOG = logging.getLogger(__name__)
# LOG.setLevel(logging.DEBUG)


class AppData:
    """A class to store app data and handle app logic"""

    def __init__(self, args):
        # Extract arguments from the request
        self.stop_id = args.get('stop_id', type=str, default=None)
        self.platforms = args.getlist('platform', type=str)
        self.line_ids = args.getlist('line_id', type=str)
        self.max_departures = args.get('max_departures', type=int,
                                       default=10)
        self.max_departure_rows = args.get('max_rows', type=int,
                                           default=6)
        self.situation_lines = None
        self.situation_gen = None
        LOG.debug("Created new AppData object, stop_id: {}, lines: {}".format(
            self.stop_id, self.line_ids))

    def get_departures(self):
        # Get new departure data
        departures = rutertider.get_departures(
            stop_id=self.stop_id, platforms=self.platforms,
            line_ids=self.line_ids, max_departures=self.max_departures)
        departures = departures[:self.max_departure_rows]
        LOG.debug("Got new departures for %s", self.stop_id)

        # Possibly update situation lines
        situation_lines = {departure.line_id for departure in departures}
        if not self.situation_lines == situation_lines:
            self.situation_lines = situation_lines
            LOG.debug("New set of situation lines: {}".format(
                self.situation_lines))

        return departures

    def _situation_generator(self):
        """A generator that yields one situation at the time"""
        while True:
            lines = []
            if self.line_ids:
                lines = self.line_ids
            elif self.situation_lines:
                lines = list(self.situation_lines)
            situations = [str(situation) for situation in
                          rutertider.get_situations(lines)]
            LOG.debug("Got new situations for lines: %s", lines)
            if not situations:
                yield ''
            for sit in situations:
                yield sit

    def next_situation(self):
        """Return the next relevant situation"""
        if self.situation_gen is None:
            # Generator hasn't been initialized yet
            self.situation_gen = self._situation_generator()
        return next(self.situation_gen)


def create_app():
    app = flask.Flask(__name__)
    app_data = None

    @app.before_request
    def create_or_update_app_data():
        """This function runs before every request"""
        # Get stop_id from request args
        stop_id = flask.request.args.get('stop_id', type=str, default=None)

        # If stop_id was not provided, show help page
        if stop_id is None:
            return flask.render_template("help.html")

        # Create global app_data instance if needed
        nonlocal app_data
        if app_data is None:
            app_data = AppData(flask.request.args)

        # If stop_id has changed, create new app_data instance
        if not app_data.stop_id == stop_id:
            app_data = AppData(flask.request.args)

    @app.route('/')
    def departures_from_stop_id():
        # Forward the query arguments to the other endpoints
        request_query = flask.request.query_string.decode()
        return flask.render_template("rutertider.html",
                                     query=flask.Markup(request_query))

    @app.route('/departure_table')
    def departure_table():
        # Get latest departures and render template
        departures = app_data.get_departures()
        return flask.render_template("departure_table.html",
                                     departures=departures)

    @app.route('/deviations')
    def deviations():
        # Wait a second so the other thread have time to
        # set the situation lines
        time.sleep(1)

        # Return next relevant situation
        return app_data.next_situation()

    return app


if __name__ == '__main__':
    # Start a Flask debugging server
    flask_app = create_app()
    LOG.setLevel(logging.DEBUG)
    flask_app.run(host='0.0.0.0', port=5000, debug=True)
