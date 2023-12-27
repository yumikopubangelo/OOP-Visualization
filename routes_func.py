# This part remains unchanged (import statements and setup_routes function)

import pandas as pd

from flask import jsonify, send_file
from visualization import AirplaneCrashes
import matplotlib.pyplot as plt





visualizer = AirplaneCrashes('C:\\Users\\vanguard\\OneDrive\\Documents\\GitHub\\OOP-Visualization\\AirplaneCrashes.csv')

        
        # Revised route function names and implementation
def get_top_routes(visualizer):
            try:
                route_data = visualizer.get_route(top_n=20)
                if route_data is not None:
                    route_count_x, route_count_y = route_data
                    return jsonify({"top_routes_crashes": {"Route": route_count_x, "crash_counts": route_count_y}})
                else:
                    return jsonify({"error": "No data available"}), 404 # Or any other appropriate status code
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
       
def get_count():
            try:
            # Code for retrieving countries and their crash counts
                countries_crashes = visualizer.get_count(top_n=20)
                return jsonify({"countries_crashes": countries_crashes.to_dict()})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
    
def get_time_of_the_day(visualizer):
    try:
        time_of_day_crashes = visualizer.get_time_of_the_day(top_n=20)
        if time_of_day_crashes is not None and not time_of_day_crashes.empty:
            return jsonify({"time_of_day_crashes": time_of_day_crashes.to_dict()})
        elif time_of_day_crashes is not None and time_of_day_crashes.empty:
            return jsonify({"error": "Empty dataset: No crash data available"}), 404
        else:
            return jsonify({"error": "No data retrieved"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
            
def visualize_time_of_the_day(visualizer, file_name='time_day_plot.png'):
    try:
        result = visualizer.visualize_time_of_the_day(AirplaneCrashes)
        if result:
            # Save the plot if 'result' is a figure object
            plt.savefig(file_name)  # Save the plot with the specified file name
            plt.close()  # Close the figure to free up memory
            return f"Plot saved successfully as '{file_name}'"
        else:
            return "Error: Plot not generated"
    except Exception as e:
        return f"Error: {str(e)}"
    
            
def visualization_type_of_aircraft():
    try:
                type_of_aircraf = visualizer.type_of_aircraft(top_n=20)
                return jsonify({"type_of_aircraft": type_of_aircraf.to_dict()})
    except Exception as e:
                return jsonify({"error": str(e)}), 500
            
def visualization_type_of_aircraft(visualizer):
    try:
        type_of_aircraft = visualizer.visualization_type_of_aircraft(top_n=20)
        return jsonify({"type_of_aircraft": type_of_aircraft.to_dict()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
            
def visualization_count(visualizer):
    try:
                countries_crashes = visualizer.visualization_count(top_n=20)
                return jsonify({"countries_crashes": countries_crashes.to_dict()})
    except Exception as e:
                return jsonify({"error": str(e)}), 500
            
def visualization_fatalities_by_year(visualizer):
    try:
                fatalities_by_year = visualizer.visualization_fatalities_by_year(top_n=20)
                return jsonify({"fatalities_by_year": fatalities_by_year.to_dict()})
    except Exception as e:
                return jsonify({"error": str(e)}), 500
    
def visualization_year(visualizer):
    try:
                year = visualizer.visualization_year(top_n=20)
                return jsonify({"year": year.to_dict()})
    except Exception as e:
                return jsonify({"error": str(e)}), 500
            
def visualization_fatalities_by_route(visualizer):
    try:
                fatalities_by_route = visualizer.visualization_fatalities_by_route(top_n=20)
                return jsonify({"fatalities_by_route": fatalities_by_route.to_dict()})
    except Exception as e:
                return jsonify({"error": str(e)}), 500
            
def visualization_operator(visualizer):
    try:
        operator = visualizer.visualization_operator(top_n=20)
        return jsonify({"operator": operator.to_dict()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
            
def visualization_fatalities_by_route(visualizer):
    try:
                fatalities_by_route = visualizer.visualization_fatalities_by_route(top_n=20)
                return jsonify({"fatalities_by_route": fatalities_by_route.to_dict()})
    except Exception as e:
                return jsonify({"error": str(e)}), 500
            

            
