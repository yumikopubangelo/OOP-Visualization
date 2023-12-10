# This part remains unchanged (import statements and setup_routes function)

from flask import jsonify
import pandas as pd
from visualization import AirplaneCrashes




        
        # Revised route function names and implementation
def get_top_routes(visualizer):
            try:
                route_data = visualizer.get_route(top_n=20)
                if route_data is not None:
                    route_count_x, route_count_y = route_data
                    return jsonify({"top_routes_crashes": {"Route": route_count_x, "crash_counts": route_count_y}})
                else:
                    return jsonify({"error": "No data available"}), 404  # Or any other appropriate status code
            except Exception as e:
                return jsonify({"error": str(e)}), 500

def get_top_operators(visualizer):
            try:
                # Code for retrieving top operators with most crashes
                top_operators = visualizer.get_top_operator(top_n=20)
                return jsonify({"top_operators_crashes": top_operators.to_dict()})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            
def get_operators_crashes(visualizer):
            try:
                # Code for retrieving operators and their crash counts
                operator_crashes = visualizer.get_operator_crashes(top_n=20)
                return jsonify({"operators_crashes": operator_crashes.to_dict()})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
def get_route(visualizer):
            try:
                route_crashes = visualizer.get_route(top_=20)
                return jsonify({"get_route": route_crashes.to_dict()})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            
def get_fatalities_by_route(visualizer):
            try:
                fatality_data = visualizer.get_fatalities_by_route(top_n=20)
                return jsonify({"fatality_data": fatality_data.to_dict()})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
       
def get_count(visualizer):
            try:
            # Code for retrieving countries and their crash counts
                countries_crashes = visualizer.get_count(top_n=20)
                return jsonify({"countries_crashes": countries_crashes.to_dict()})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
    
def get_time_of_the_day(visualizer):
            try:
                time_of_day_crashes = visualizer.get_time_of_the_day(top_n=20)
                return jsonify({"time_of_day_crashes": time_of_day_crashes.to_dict()})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            

            

            
