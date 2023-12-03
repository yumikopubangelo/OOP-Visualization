from flask import jsonify
from visualization import AirplaneCrashes

def setup_routes(app):
    visualizer = AirplaneCrashes()

    @app.route('/top_operators_crashes', methods=['GET'])
    def get_top_operators():
        try:
            top_operators = visualizer.get_top_operator(top_n=20)
            top_operators_dict = top_operators.to_dict()
            return jsonify({"top_operators_crashes": top_operators_dict})
        except Exception as e:
            return jsonify({"error": str(e)}, 500)
    @app.route('/top_operator', methods = ['GET'])
    def get_operator():
        try:
            op_fatalities = visualizer.get_route(top_n=20)
            op_fatalities_dict = op_fatalities.to_dict()
            return jsonify({"operator": op_fatalities_dict})
        except Exception as e:
            return jsonify({"error": str(e)}, 500)
    