import logging

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
        LOG.debug("Created new AppData object, lines: {}".format(
            self.line_ids))

    def get_departures(self):
        # Get new departure data
        departures = rutertider.get_departures(
            stop_id=self.stop_id, platforms=self.platforms,
            line_ids=self.line_ids, max_departures=self.max_departures)
        departures = departures[:self.max_departure_rows]
        LOG.debug("Got new departures for %s", self.stop_id)

        # Possibly update situation generator
        situation_lines = {departure.line_id for departure in departures}
        self.update_situation_generator(situation_lines)

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

    def update_situation_generator(self, situation_lines):
        # Update the situation generator if the lines changed
        if not self.situation_lines == situation_lines:
            self.situation_lines = situation_lines
            LOG.debug("New set of situation lines: {}".format(
                self.situation_lines))
            # self.situation_gen = self._situation_generator()

    def next_situation(self):
        """Return the next relevant situation"""
        if self.situation_gen is None:
            # Generator hasn't been initialized yet
            if self.situation_lines is None:
                # Departures haven't been pulled yet
                self.get_departures()
            self.situation_gen = self._situation_generator()
        return next(self.situation_gen)


def create_app():
    app = flask.Flask(__name__)
    app_data = None

    @app.route('/')
    def departures_from_stop_id():
        # Create a new AppData instance based in the query arguments
        nonlocal app_data
        app_data = AppData(flask.request.args)

        # If stop_id was not provided, show help page
        if app_data.stop_id is None:
            return flask.render_template("help.html")

        # Forward the query arguments to the other endpoints
        request_query = flask.request.query_string.decode()
        return flask.render_template("rutertider.html",
                                     query=flask.Markup(request_query))

    @app.route('/departure_table')
    def departure_table():
        # If arguments haven't been parsed yet
        nonlocal app_data
        if app_data is None:
            app_data = AppData(flask.request.args)

        # Get latest departures and render template
        departures = app_data.get_departures()
        return flask.render_template("departure_table.html",
                                     departures=departures)

    @app.route('/deviations')
    def deviations():
        # If arguments haven't been parsed yet
        nonlocal app_data
        if app_data is None:
            app_data = AppData(flask.request.args)

        # Return next relevant situation
        return app_data.next_situation()

    return app


app = create_app()

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
