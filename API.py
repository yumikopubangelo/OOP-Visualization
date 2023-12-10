from flask import Flask, jsonify,request
import os
from visualization import AirplaneCrashes
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from functools import wraps
from route import get_route, setup_routes



app = Flask(__name__)

plot_counter = 0  # Initialize a counter for unique filenames
top_n= 20
data_frame = pd.read_csv('C:\\Users\\vanguard\\OneDrive\\Documents\\GitHub\\OOP-Visualization\\AirplaneCrashes.csv')  # Replace 'path_to_your_data.csv' with your actual data file
base_dir = 'C:\\Users\\vanguard\\OneDrive\\Documents\\GitHub\\OOP-Visualization'
visualizer = AirplaneCrashes(base_dir, data_frame)

setup_routes(app, visualizer)

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
    sanitized_path = os.path.abspath(os.path.join(base_dir, file_path))
    if not sanitized_path.startswith(base_dir):
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
        file.save(os.path.join(base_dir, file.filename))
        df = read_sanitized_csv(file.filename)
        return jsonify({'message': 'file uploaded successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/route_data', methods=['GET'])
def visualization_route():
    """
    This function visualizes the top routes in terms of crashes and processes top operators' data.
    """
    try:
        global plot_counter      
        route_count_x, route_count_y = visualizer.get_route()

        plt.figure(figsize=(30, 20))
        plt.barh(route_count_x[:20], route_count_y[:20])
        plt.xlabel('Crashes')
        plt.title(f'Top {top_n} Route')

        plot_counter += 1
        plot_file = f"route_visualization_{plot_counter}.png"

        # Call the function to get route data
        route_data = get_route()

        # Handle the case where route_data is None
        if route_data is None:
            return jsonify({'error': 'No route data available'}), 404

        # Further processing of route data
        # For example, assuming route_data is a dictionary
        # Extracting relevant information from the data
        routes = route_data.get("get_route", {})
        route_names = list(routes.keys())
        route_counts = list(routes.values())

        # Further visualization or processing with route data
        # For instance, plotting the routes and their crash counts
        plt.figure(figsize=(12, 8))
        sns.barplot(x=route_counts, y=route_names)
        plt.xlabel('Crash Counts')
        plt.ylabel('Routes')
        plt.title('Top Routes and Their Crash Counts')

        # Save the plot with a unique filename
        plot_counter += 1
        plot_file_routes = f"routes_visualization_{plot_counter}.png"
        plt.savefig(os.path.join(base_dir, plot_file_routes))
        plt.clf()  # Clear the current figure

        return jsonify({
            'visualization_path_routes': plot_file_routes,
            'visualization_path_operators': plot_file
        })
    except Exception as e:
        return jsonify({'error': str(e)})
 
@app.route('/visualization/operator', methods = ['GET'])       
def visualization_operator():
        """
        This function visualizes the top operators in terms of fatalities.
        """
        try:
            global plot_counter  
            op_fatalities_x , op_fatalities_y = visualizer.get_operator()

       
            

            plt.figure(figsize=(30,20))
            plt.barh (op_fatalities_x[:20], op_fatalities_y[:20])
            plt.xlabel ('Fatalities')
            plt.title(f"Top {top_n} operator")
       
            plot_counter += 1
            plot_file = f"route_visualization_{plot_counter}.png"

            # Save the plot with a unique filename
            plt.savefig(os.path.join(base_dir, plot_file))
            plt.clf()  # Clear the current figure
            
            return jsonify({'visualization_path': plot_file})
        
        except Exception as e:
            return jsonify({'error': str(e)})  
        
     
@app.route('/visualization/fatalities/by/route', methods = ['GET']) 
def visualization_fatalities_by_route():
        """
        This function visualizes the fatalities by route.
        """
        try:
            global plot_counter
            route_fatalities = visualizer.get_fatalities_by_route()
            if route_fatalities is not None:
                route_fatalities[:20].plot(kind = 'barh')
                plt.title('Number of Fatalities per Route')
                plt.xlabel('Passengers')    
                plot_counter += 1
                plot_file = f"route_visualization_{plot_counter}.png"

            # Save the plot with a unique filename
                plt.savefig(os.path.join(base_dir, plot_file))
                plt.clf()  # Clear the current figure
                return jsonify({'visualization_path': plot_file})
        except Exception as e:
            return jsonify({'error': str(e)})
@app.route('/visualization/year', methods = ['GET'])       
def visualization_year():
        """
        This function visualizes the distribution of crashes by year.
        """
        try:
            global plot_counter
            years = pd.to_datetime(visualizer.df['Date']).dt.year
            year_count = years.value_counts().head(top_n).sort_values(ascending=False)

            plt.figure(figsize=(10, 6))
            sns.histplot(years, kde=True, color='green')
            plt.xlabel('Year')
            plt.title(f'Top {top_n} Year Distribution')

            plot_counter += 1
            plot_file = f"route_visualization_{plot_counter}.png"

            # Save the plot with a unique filename
            plt.savefig(os.path.join(base_dir, plot_file))
            plt.clf()  # Clear the current figure
            return jsonify({'visualization_path': plot_file})

        except Exception as e:
            return jsonify({'error': str(e)})
@app.route('/visualization/fatalities/by/year', methods = ['GET']) 
def visualization_fatalities_by_year():
        """
        This function visualizes the fatalities and number of individuals aboard per year.
        """
        try:
            global plot_counter
            # Assuming 'Date' column exists in your DataFrame
            visualizer.df['Year'] = pd.to_datetime(visualizer.df['Date']).dt.year
       
            # Grouping by 'Year' and summing 'Fatalities' and 'Aboard'
            fatalities_by_year = visualizer.df.groupby('Year')[['Fatalities', 'Aboard']].sum()

            # Plotting fatalities and number of individuals aboard per year
            fatalities_by_year.plot(kind='bar', figsize=(40, 20))
            plt.xlabel('Year')
            plt.ylabel('Count')
            plt.title('Fatalities and Aboard per Year')
            plot_counter += 1
            plot_file = f"route_visualization_{plot_counter}.png"

            # Save the plot with a unique filename
            plt.savefig(os.path.join(base_dir, plot_file))
            plt.clf()  # Clear the current figure
            
            return jsonify({'visualization_path': plot_file})

        except Exception as e:
            return jsonify({'error': str(e)})
@app.route('/visualization/count', methods = ['GET'])        
def visualization_count():
        """
        This function visualizes the count of crashes by region.
        """
        try:
            global plot_counter
            countries_grouped = visualizer.get_count()
       
            plt.figure(figsize=(10, 6))
            sns.barplot(x=countries_grouped['count'][:top_n], y=countries_grouped.index[:top_n])
            plt.xlabel('Count')
            plt.ylabel('Region')
            plt.title(f'Top {top_n} Regions in Airplane Crashes')
            
            plot_counter += 1
            plot_file = f"route_visualization_{plot_counter}.png"

            # Save the plot with a unique filename
            plt.savefig(os.path.join(base_dir, plot_file))
            plt.clf()  # Clear the current figure
            return jsonify({'visualization_path': plot_file})

        
        except Exception as e:
            return jsonify({'error': str(e)})
@app.route('/visualization/type/of/aircraft', methods = ['GET'])        
def visualization_type_of_aircraft():
    
    try:
        global plot_counter
        type_count=df.groupby(['Type']).count().sort_values('index',ascending=False)
        tc_x=type_count.index
        tc_y=type_count['index']
        plt.ylabel('TYPE OF AIRCRAFT')
        plt.barh(tc_x[:20],tc_y[:20])
        plt.title(f'Top {top_n} Type Of Aircraft')
        plt.xlabel('Crashes')
        
        plot_counter += 1
        plot_file = f"route_visualization_{plot_counter}.png"

            # Save the plot with a unique filename
        plt.savefig(os.path.join(base_dir, plot_file))
        plt.clf()  # Clear the current figure
        return jsonify({'visualization_path': plot_file})
    except Exception as e:
            return jsonify({'error': str(e)}) 
@app.route('/visualization/time/of/the/day', methods = ['GET'])     
def visualization_time_of_the_day():
        try:
            global plot_counter
            time_count= visualizer.get_time_of_the_day()

            if time_count is not None:      
                time_count= time_count['Hour'].value_counts().sort_index()
                time_count.plot(kind='bar')
                plt.xlabel('Hour of the Day')
                plt.ylabel('Crash Count')
                plt.title('Crashes by Time of Day')
                
                plot_counter += 1
                plot_file = f"route_visualization_{plot_counter}.png"

            # Save the plot with a unique filename
                plt.savefig(os.path.join(base_dir, plot_file))
                plt.clf()  # Clear the current figure
                return jsonify({'visualization_path': plot_file})
        except Exception as e:
            return jsonify({'error': str(e)})   
        
if __name__ == '__main__':
    app.run(debug=True)
        