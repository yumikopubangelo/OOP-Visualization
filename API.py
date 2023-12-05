from flask import Flask, jsonify,request
from routes import AirplaneCrashes
import os
import pandas as pd
import matplotlib.pyplot as plt
from functools import wraps

app = Flask(__name__)

base_directory = 'C:\\Users\\vanguard\\OneDrive\\Documents\\GitHub\\OOP-Visualization' 

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

def sanitize_path(file_path):
    sanitized_path = os.path.abspath(os.path.join(base_directory, file_path))
    if not sanitized_path.startswith(base_directory):
        raise ValueError('Invalid file path')
    return sanitized_path

def read_sanitized_csv(user_input):
    file_path = sanitize_path(user_input)
    df = pd.read_csv(file_path)
    return df

user_input = input ("enter file name:")
try:
    df = read_sanitized_csv(user_input)
    print(df.head())  # Displaying a preview of the DataFrame
except ValueError as e:
    print(f"Error: {e}")
    
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"message": "No file part"})
        file = request.files['file']
        if file.filename == '':
            return jsonify ({'error': 'No selected file'})
        file.save(os.path.join(base_directory, file.filename))
        df = read_sanitized_csv(file.filename)
        return jsonify({'message': 'file uploaded successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/visualization/route', methods = ['GET'])
def visualization_route(self, top_n=20):
        """
        This function visualizes the top routes in terms of crashes.
        """
        try:      
            route_count_x, route_count_y= self.get_route()
  
            plt.figure(figsize=(30,20))
            plt.barh (route_count_x[:20], route_count_y[:20])
            plt.xlabel ('Crashes')
            plt.title(f'Top {top_n} Route ')

            plot_file = os.path.join(base_directory, 'route_visualization.png')
            plt.savefig(plot_file)
            
            return jsonify({'visualization_path': plot_file})
        except Exception as e:
            return jsonify({'error': str(e)})
        
def visualization_operator(self, top_n=20):
        """
        This function visualizes the top operators in terms of fatalities.
        """
        try:
            op_fatalities_x , op_fatalities_y = self.get_operator()

       
            

            plt.figure(figsize=(30,20))
            plt.barh (op_fatalities_x[:20], op_fatalities_y[:20])
            plt.xlabel ('Fatalities')
            plt.title(f"Top {top_n} operator")
       
            plot_file = os.path.join(base_directory, 'operator.png')
            plt.savefig(plot_file)
            
            return jsonify({'visualization_path': plot_file})
        
        except AttributeError as e:
            return jsonify({'error': str(e)})
            
