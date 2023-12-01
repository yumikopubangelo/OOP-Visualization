from flask import jsonify
from visualization import AirplaneCrashes

def setup_routes(app):
    visualizer = AirplaneCrashes()

    @app.route('/top_operators_crashes', methods=['GET'])
    def get_top_operators_crashes():
        try:
            top_operators = visualizer.get_top_operator(top_n=20)
            return jsonify({"top_operators_crashes": top_operators.to_dict()})
        except Exception as e:
            return jsonify({"error": str(e)}, 500)