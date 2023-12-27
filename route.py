from flask import jsonify, request
import os 
from time import time
import pandas as pd
from visualization import AirplaneCrashes
from routes_func import (
    get_top_routes,
    get_top_operators,
    get_operators_crashes,
    get_route,
    get_fatalities_by_route,
    get_count,
    get_time_of_the_day,
    visualize_time_of_the_day,
    visualization_type_of_aircraft,
    visualization_count,
    visualization_fatalities_by_year,
    visualization_year,
    visualization_fatalities_by_route,
    visualization_operator,
    visualization_fatalities_by_route,
)



visualizer_routes= AirplaneCrashes('C:\\Users\\vanguard\\OneDrive\\Documents\\GitHub\\OOP-Visualization\\AirplaneCrashes.csv')


def sanitize_path(file_path, base_dir):
        sanitized_path = os.path.abspath(os.path.join(base_dir, file_path))
        if not sanitized_path.startswith(base_dir):
            raise ValueError('Invalid file path')
        return sanitized_path

def read_sanitized_csv(file_path, base_dir):
    try:
        sanitized_path = sanitize_path(file_path, base_dir)
        df = pd.read_csv(sanitized_path)
        print(df.head()) # Displaying a preview of the DataFrame
        return df
    except ValueError as e:
        print(f"Error: {e}")


user_input = input("Enter file name: ")
base_dir = 'C:\\Users\\vanguard\\OneDrive\\Documents\\GitHub\\OOP-Visualization' # Define your base directory
def validate_path(file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError('File not found')
        
        if not file_path.lower().endswith('.csv'):
            raise ValueError('invalid file extension. expected a CSV file.')
        
        max_file_size = 10 * 1024 * 1024
        if os.path.getsize(file_path) > max_file_size:
            raise ValueError('File size exceeds the limit (10MB).')
        ##Date,Time,Location,Operator,Flight #,Route,Type,Registration,cn/In,Aboard,Fatalities,Ground,Summary
        expected_columns = ['Date', 'Time', 'Location', 'Operator', 'Flight #', 'Route', 'Type', 'Registration', 'cn/In', 'Aboard', 'Fatalities', 'Ground', 'Summary']
        df = pd.read_csv(file_path)
        if not all(col in df.columns for col in expected_columns):
            raise ValueError('CSV file does not contain expected columns')



def setup_routes(app, visualizer_routes):
   @app.route('/upload', methods=['POST'])
   def upload_file():
       try:
           if request.method == 'POST':
               if 'file' not in request.files:
                   return jsonify({"error": "No file part"})
               
               file = request.files['file']
               
               if file.filename == '':
                   return jsonify({"error": "No selected file"})
               
               if file and file.filename.endswith('.csv'):
                   file_path = os.path.join(base_dir, file.filename)
                   file.save(file_path)
                   
                   # Validate and read the CSV file
                   validate_path(file_path)
                   df = read_sanitized_csv(file_path, base_dir)
                   
                   # Optionally, perform operations with the DataFrame 'df'
                   
                   return jsonify({'message': 'File uploaded successfully'})
               else:
                   return jsonify({"error": "Invalid file format. Expected a CSV file"})
       except Exception as e:
           return jsonify({'error': str(e)})

   @app.route('/top_routes_crashes', methods=['GET'])
   def top_routes_crashes():
       return get_top_routes(visualizer_routes)

   @app.route('/top_operators', methods=['GET'])
   def top_operators():
       return get_top_operators(visualizer_routes)

   @app.route('/operator_crashes', methods=['GET'])
   def operator_crashes():
       return get_operators_crashes(visualizer_routes)

   @app.route('/get_route', methods=['GET'])
   def route():
       return get_route(visualizer_routes)

   @app.route('/fatalities_by_route', methods=['GET'])
   def fatalities_by_route():
       return get_fatalities_by_route(visualizer_routes)

   @app.route('/count', methods=['GET'])
   def count():
       return get_count(visualizer_routes)

   @app.route('/time_of_the_day', methods=['GET'])
   def time_of_the_day():
        try:
            result = get_time_of_the_day(visualizer_routes)
            return result  # Return the JSON-formatted response directly
        except Exception as e:
            return jsonify({"error": str(e)}), 500
   
   
   @app.route('/type_of_aircraft',methods=['GET'])
   def type_of_aircraft():
       return visualization_type_of_aircraft(visualizer_routes)
   
   @app.route('/countries',methods=['GET'])
   def countries():
       return visualization_count(visualizer_routes)
   
   @app.route('/fatalities_by_year',methods=['GET'])
   def fatalities_by_year():
        return visualization_fatalities_by_year(visualizer_routes)
   
   @app.route('/visualize')
   def another_function():
       try:
           # Instantiate or obtain the 'visualizer' object here (depends on your code structure)
           visualizer = AirplaneCrashes() # Instantiate your Visualizer class or get the object
    
           # Call visualize_time_of_the_day() function and handle its output
           result = visualize_time_of_the_day(visualizer) # Pass 'visualizer' object
           # Do something with the result (e.g., send it to an API endpoint, save to a file, etc.)
           return result # Return the result to the route
           
       except Exception as e:
           # Handle exceptions if needed
           return f"Error: {str(e)}"


   app.add_url_rule('/visualize_time_of_day', 'visualize_time_of_day', visualize_time_of_the_day, methods=['GET'])
   # Add more routes as needed...

   return app