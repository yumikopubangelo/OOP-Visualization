# This part remains unchanged (import statements and setup_routes function)

from flask import jsonify
import pandas as pd

class AirplaneCrashes:
    def __init__(self, data_frame, base_dir):
        """
        This function initializes the AirplaneCrashes class with a DataFrame.
        """
        self.data_frame = data_frame # Initialize the class with the provided DataFrame
        self.base_directory = base_dir
    base_directory = 'C:\\Users\\vanguard\\OneDrive\\Documents\\GitHub\\OOP-Visualization'


def setup_routes(app, visualizer):
        
    # Revised route function names and implementation
    @app.route('/top_routes_crashes', methods=['GET'])
    def get_top_routes():
        try:
            # Code for retrieving top routes with most crashes
            top_routes_x, top_routes_y = visualizer.get_top_routes(top_n=20)
            return jsonify({"top_routes_crashes": {"routes": top_routes_x, "crash_counts": top_routes_y}})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/top_operators', methods=['GET'])
    def get_top_operators():
        try:
            # Code for retrieving top operators with most crashes
            top_operators = visualizer.get_top_operators(top_n=20)
            return jsonify({"top_operators_crashes": top_operators.to_dict()})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/operators_crashes', methods=['GET'])
    def get_operators_crashes():
        try:
            # Code for retrieving operators and their crash counts
            operator_crashes = visualizer.get_operator_crashes(top_n=20)
            return jsonify({"operators_crashes": operator_crashes.to_dict()})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    @app.route ('/route_crashes', methods = ['GET'])  
    def get_route():
        try:
            route_crashes = visualizer.get_route(top_=20)
            return jsonify({"get_route": route_crashes.to_dict()})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    @app.route ('/fatality_data', methods = ['GET'])    
    def get_fatalities_by_route():
        try:
            fatality_data = visualizer.get_fatalities_by_route(top_n=20)
            return jsonify({"fatality_data": fatality_data.to_dict()})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    @app.route ('/countries_crashes', methods = ['GET'])     
    def get_count():
        try:
        # Code for retrieving countries and their crash counts
            countries_crashes = visualizer.get_count(top_n=20)
            return jsonify({"countries_crashes": countries_crashes.to_dict()})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    @app.route ('/time_of_day_crashes', methods = ['GET'])    
    def get_time_of_the_day():
        try:
            time_of_day_crashes = visualizer.get_time_of_the_day(top_n=20)
            return jsonify({"time_of_day_crashes": time_of_day_crashes.to_dict()})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    return app
        

        
