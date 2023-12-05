from flask import Flask, jsonify,request
from routes import AirplaneCrashes
import os
import seaborn as sns
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
        
        except Exception as e:
            return jsonify({'error': str(e)})  
        
     

def visualization_fatalities_by_route(self, top_n=20):
        """
        This function visualizes the fatalities by route.
        """
        try:
            route_fatalities = self.get_fatalities_by_route()
            if route_fatalities is not None:
                route_fatalities[:20].plot(kind = 'barh')
                plt.title('Number of Fatalities per Route')
                plt.xlabel('Passengers')    
                plot_file = os.path.join({'visualization_fatalities_by_route': plot_file})
                plt.savefig(plot_file)
                return jsonify({'visualization_path': plot_file})
        except Exception as e:
            return jsonify({'error': str(e)})
        
def visualization_year(self, top_n=20):
        """
        This function visualizes the distribution of crashes by year.
        """
        try:
            years = pd.to_datetime(self.df['Date']).dt.year
            year_count = years.value_counts().head(top_n).sort_values(ascending=False)

            plt.figure(figsize=(10, 6))
            sns.histplot(years, kde=True, color='green')
            plt.xlabel('Year')
            plt.title(f'Top {top_n} Year Distribution')

            plot_file = os.path.join({'visualization_year': plot_file})
            plt.savefig(plot_file)
            return jsonify({'visualization_path': plot_file})

        except Exception as e:
            return jsonify({'error': str(e)})
 
def visualization_fatalities_by_year(self, top_n=20):
        """
        This function visualizes the fatalities and number of individuals aboard per year.
        """
        try:
            # Assuming 'Date' column exists in your DataFrame
            self.df['Year'] = pd.to_datetime(self.df['Date']).dt.year
       
            # Grouping by 'Year' and summing 'Fatalities' and 'Aboard'
            fatalities_by_year = self.df.groupby('Year')[['Fatalities', 'Aboard']].sum()

            # Plotting fatalities and number of individuals aboard per year
            fatalities_by_year.plot(kind='bar', figsize=(40, 20))
            plt.xlabel('Year')
            plt.ylabel('Count')
            plt.title('Fatalities and Aboard per Year')
            plot_file = os.path.join({'visualization_fatalities_by_year': plot_file})
            plt.savefig(plot_file)
            
            return jsonify({'visualization_path': plot_file})

        except Exception as e:
            return jsonify({'error': str(e)})
        
def visualization_count(self, top_n=20):
        """
        This function visualizes the count of crashes by region.
        """
        try:
            countries_grouped = self.get_count()
       
            plt.figure(figsize=(10, 6))
            sns.barplot(x=countries_grouped['count'][:top_n], y=countries_grouped.index[:top_n])
            plt.xlabel('Count')
            plt.ylabel('Region')
            plt.title(f'Top {top_n} Regions in Airplane Crashes')
            
            plot_file = os.path.join({'visualization_count': plot_file})
            plt.savefig(plot_file)
            return jsonify({'visualization_path': plot_file})

        
        except Exception as e:
            return jsonify({'error': str(e)})
        
def visualization_type_of_aircraft(self, top_n=20):
    
    try:
        type_count=df.groupby(['Type']).count().sort_values('index',ascending=False)
        tc_x=type_count.index
        tc_y=type_count['index']
        plt.ylabel('TYPE OF AIRCRAFT')
        plt.barh(tc_x[:20],tc_y[:20])
        plt.title(f'Top {top_n} Type Of Aircraft')
        plt.xlabel('Crashes')
        
        plot_file = os.path.join({'visualization_type_of_aircraft': plot_file})
        plt.savefig(plot_file)
        return jsonify({'visualization_path': plot_file})
    except Exception as e:
            return jsonify({'error': str(e)}) 
        
def visualization_time_of_the_day(self, top_n=20):
        try:
            time_count= self.get_time_of_the_day()

            if time_count is not None:      
                time_count= time_count['Hour'].value_counts().sort_index()
                time_count.plot(kind='bar')
                plt.xlabel('Hour of the Day')
                plt.ylabel('Crash Count')
                plt.title('Crashes by Time of Day')
                
                plot_file = os.path.join({'visualization_time_of_the_day' : plot_file})
                plt.savefig(plot_file)
                return jsonify({'visualization_path': plot_file})
        except Exception as e:
            return jsonify({'error': str(e)})    
            
