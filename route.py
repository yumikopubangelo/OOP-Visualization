from routes_func import (
    get_top_routes,
    get_top_operators,
    get_operators_crashes,
    get_route,
    get_fatalities_by_route,
    get_count,
    get_time_of_the_day,
)

def setup_routes(app, visualizer):
    @app.route('/top_routes_crashes', methods=['GET'])
    def top_routes_crashes():
        return get_top_routes(visualizer)

    @app.route('/top_operators', methods=['GET'])
    def top_operators():
        return get_top_operators(visualizer)

    @app.route('/operator_crashes', methods=['GET'])
    def operator_crashes():
        return get_operators_crashes(visualizer)

    @app.route('/get_route', methods=['GET'])
    def get_route():
        return get_route(visualizer)

    @app.route('/fatalities_by_route', methods=['GET'])
    def fatalities_by_route():
        return get_fatalities_by_route(visualizer)

    @app.route('/count', methods=['GET'])
    def count():
        return get_count(visualizer)

    @app.route('/time_of_the_day', methods=['GET'])
    def time_of_the_day():
        return get_time_of_the_day(visualizer)

    # Add more routes as needed...

    return app
