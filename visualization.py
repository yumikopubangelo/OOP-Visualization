from flask import jsonify, send_file, Flask
import numpy as np
from flask import jsonify
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import io
import base64
from functools import wraps

plot_counter = 0  # Initialize a counter for unique filenames



            
            

def visualization_lastWord(string):
    """
    This function extracts the last word from a string.
    """
    lis = list(str(string).split(" "))
    length = len(lis)
    return lis[length-1]



def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error occurred:{e}")
    return wrapper


        

            
def generate_bar_chart(self, column):
                if column not in self.data.columns:
                    return {"error": f"Column '{column}' not found in the dataset"}
                
                column_data = self.data[column]
                # Replace this with your actual visualization logic
                # For example, generating a bar chart
                chart_data = column_data.value_counts().to_dict()
                
                return {"bar_chart": chart_data}

def generate_statistics(self):
                # Replace this with your actual statistical analysis logic
                # For example, computing mean, median, etc.
                statistics = {
                    "mean": self.data.mean().to_dict(),
                    "median": self.data.median().to_dict(),
                    "std": self.data.std().to_dict()
                }
                return {"statistics": statistics}

from flask import jsonify, send_file, Flask
import numpy as np
from flask import jsonify
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import io
import base64
from functools import wraps

plot_counter = 0  # Initialize a counter for unique filenames



            
            

def visualization_lastWord(string):
    """
    This function extracts the last word from a string.
    """
    lis = list(str(string).split(" "))
    length = len(lis)
    return lis[length-1]



def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error occurred:{e}")
    return wrapper


        

            
def generate_bar_chart(self, column):
                if column not in self.data.columns:
                    return {"error": f"Column '{column}' not found in the dataset"}
                
                column_data = self.data[column]
                # Replace this with your actual visualization logic
                # For example, generating a bar chart
                chart_data = column_data.value_counts().to_dict()
                
                return {"bar_chart": chart_data}

def generate_statistics(self):
                # Replace this with your actual statistical analysis logic
                # For example, computing mean, median, etc.
                statistics = {
                    "mean": self.data.mean().to_dict(),
                    "median": self.data.median().to_dict(),
                    "std": self.data.std().to_dict()
                }
                return {"statistics": statistics}



class AirplaneCrashes:
    def __init__(self, data_path='AirplaneCrashes.csv'):
        """
        Initializes the AirplaneCrashes class with a DataFrame and base directory.
        """
        self.df = None
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.load_data(data_path)

    @staticmethod
    def handle_exceptions(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Error occurred: {e}")
        return wrapper

    @handle_exceptions
    def load_data(self, data_path='AirplaneCrashes.csv'):
        try:
            self.df = pd.read_csv(data_path)
        except Exception as e:
            print(f"Error reading CSV: {e}")
    

            

    @handle_exceptions
    def get_top_operator(self, top_n=20):
        """
        Retrieves the top operators accounting for crashes.
        """
        if 'Operator' not in self.df.columns:
            raise ValueError("Column 'Operator' not found in DataFrame")

        operator_counts = self.df['Operator'].value_counts().dropna()
        top_operators = operator_counts.head(top_n)
        return top_operators
       



    @handle_exceptions
    def get_operator(self, top_n=20):
        try:
            op_fatalities = self.df.groupby('Operator')['Fatalities'].sum().dropna() 
            top_op_fatalities = op_fatalities.nlargest(top_n)
            op_fatalities_x = top_op_fatalities.index.tolist()
            op_fatalities_y = top_op_fatalities.tolist()
    
            return op_fatalities_x, op_fatalities_y
        
        except (KeyError, ValueError) as e:
            print(f"Error occurred:{e}")
            return None
        except AttributeError as e:
            print(f"AttributeError occurred:{e}")
            raise




    @handle_exceptions
    def get_route(self, top_n=20):
        try:
            if 'Route' not in self.df.columns:
                raise ValueError("Column 'Route' not found in DataFrame")
            route_count = self.df['Route'].value_counts().sort_values(ascending = False)
            top_route_counts = route_count.head(top_n)

            route_count_x= top_route_counts.index.tolist()
            route_count_y = top_route_counts.tolist()
            return route_count_x,route_count_y

        except (KeyError, ValueError) as e:
            print(f"Error occurred:{e}")
            return None
        except AttributeError as e:
            print(f'Attribute Error Occurred {e}')
            raise
            
        

    @handle_exceptions 
    def get_fatalities_by_route(self,top_n=20):
        try:
            route_fatalities = self.df.groupby ('Route')['Fatalities'].sum().nlargest(top_n)
            return route_fatalities
            
        except (KeyError, ValueError) as e:
            print(f"Error occurred:{e}")
            return None
        except AttributeError as e:
            print(f'Attribute Error Occurred {e}')
            raise
    
    

    @handle_exceptions
    def get_count(self, top_n=20):
        try:
            last_words = self.df['Location'].str.split().str[-1]
            countries_df = pd.DataFrame({'Region': last_words, 'count': np.ones(len(self.df))})
            countries_grouped = countries_df.groupby('Region').count().sort_values('count', ascending=False)
            return countries_grouped
        except (KeyError, ValueError) as e:
            print(f"Error occurred:{e}")
            return None
        except AttributeError as e:
            print(f"AttributeError occurred:{e}")
            raise
    
   
  
            

    @handle_exceptions
    def get_time_of_the_day(self, top_n=20):
        try:
            # Assuming you have a 'Time' column in your DataFrame
            df = self.df.dropna(subset=['Time']).copy()
            df['Hour'] = df['Time'].astype(str).str[:2]  # Extract hour from the 'Time' column
            df = df[df['Hour'].str.isnumeric()]  # Filter valid hour entries
            
            # Count crashes for each hour
            time_of_day_crashes = df['Hour'].value_counts().head(top_n)
            
            return time_of_day_crashes.to_dict()  # Return crash counts as a dictionary
        except Exception as e:
            # Handle exceptions accordingly
            print(f"Error: {str(e)}")
            return None
        
    
    
                
    def visualization_operator(self, top_n=20):
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
            plt.savefig(os.path.join(self.df, plot_file))
            plt.clf()  # Clear the current figure
            
            return jsonify({'visualization_path': plot_file})
        
        except Exception as e:
            return jsonify({'error': str(e)})  
        
    def visualization_fatalities_by_route(self, top_n=20):
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
                plt.savefig(os.path.join(self.df, plot_file))
                plt.clf()  # Clear the current figure
                return jsonify({'visualization_path': plot_file})
        except Exception as e:
            return jsonify({'error': str(e)})
        
    def visualization_year(self, top_n=20):
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
            plt.savefig(os.path.join(self.df, plot_file))
            plt.clf()  # Clear the current figure
            return jsonify({'visualization_path': plot_file})
        except Exception as e:
            return jsonify({'error': str(e)})
        
    def visualization_fatalities_by_year(self, top_n=20):
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
            plt.savefig(os.path.join(self.df, plot_file))
            plt.clf()  # Clear the current figure
            
            return jsonify({'visualization_path': plot_file})

        except Exception as e:
            return jsonify({'error': str(e)})
    
    def visualization_count(self, top_n=20):
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
            plt.savefig(os.path.join(self.df, plot_file))
            plt.clf()  # Clear the current figure
            return jsonify({'visualization_path': plot_file})
        except Exception as e:
            return jsonify({'error': str(e)})
        
    def visualization_type_of_aircraft(self, top_n=20):
    
        try:
            global plot_counter
            type_count=self.df.groupby(['Type']).count().sort_values('index',ascending=False)
            tc_x=type_count.index
            tc_y=type_count['index']
            plt.ylabel('TYPE OF AIRCRAFT')
            plt.barh(tc_x[:20],tc_y[:20])
            plt.title(f'Top {top_n} Type Of Aircraft')
            plt.xlabel('Crashes')
        
            plot_counter += 1
            plot_file = f"route_visualization_{plot_counter}.png"

            # Save the plot with a unique filename
            plt.savefig(os.path.join(self.df, plot_file))
            plt.clf()  # Clear the current figure
            return jsonify({'visualization_path': plot_file})
        except Exception as e:
            return jsonify({'error': str(e)}) 
        
  
    def visualize_time_of_the_day(self, top_n=20):
        try:
            time_of_day_crashes = visualizer.get_time_of_the_day(top_n=top_n)

            if time_of_day_crashes is not None:
                    # Assuming time_of_day_crashes is a pandas DataFrame with 'Hour' and 'Crash Count' columns
                    plt.bar(time_of_day_crashes['Hour'])
                    plt.xlabel('Hour of the Day')
                    plt.ylabel('Crash Count')
                    plt.title('Crash Count by Time of Day')
                    
                    # Save the plot with a unique filename
                    plot_file = 'C:\\Users\\vanguard\\OneDrive\\Documents\\GitHub\\OOP-Visualization\\time_of_the_day.png'

                    plt.savefig(plot_file)
                    plt.close()  # Close the figure to free up memory

                    return plot_file  # Return the file name or full file path
                    
        
            else:
                    return jsonify({"error": "No data available"}), 404
                
           
        except Exception as e:
                return jsonify({"error": str(e)}), 500
            
    
        
   
visualizer = AirplaneCrashes('C:\\Users\\vanguard\\OneDrive\\Documents\\GitHub\\OOP-Visualization\\AirplaneCrashes.csv')


class AirplaneCrashes:
    def __init__(self, data_path='AirplaneCrashes.csv'):
        """
        Initializes the AirplaneCrashes class with a DataFrame and base directory.
        """
        self.df = None
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.load_data(data_path)

    @staticmethod
    def handle_exceptions(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Error occurred: {e}")
        return wrapper

    @handle_exceptions
    def load_data(self, data_path='AirplaneCrashes.csv'):
        try:
            self.df = pd.read_csv(data_path)
        except Exception as e:
            print(f"Error reading CSV: {e}")

            

    @handle_exceptions
    def get_top_operator(self, top_n=20):
        """
        Retrieves the top operators accounting for crashes.
        """
        if 'Operator' not in self.df.columns:
            raise ValueError("Column 'Operator' not found in DataFrame")

        operator_counts = self.df['Operator'].value_counts().dropna()
        top_operators = operator_counts.head(top_n)
        return top_operators
       



    @handle_exceptions
    def get_operator(self, top_n=20):
        try:
            op_fatalities = self.df.groupby('Operator')['Fatalities'].sum().dropna() 
            top_op_fatalities = op_fatalities.nlargest(top_n)
            op_fatalities_x = top_op_fatalities.index.tolist()
            op_fatalities_y = top_op_fatalities.tolist()
    
            return op_fatalities_x, op_fatalities_y
        
        except (KeyError, ValueError) as e:
            print(f"Error occurred:{e}")
            return None
        except AttributeError as e:
            print(f"AttributeError occurred:{e}")
            raise




    @handle_exceptions
    def get_route(self, top_n=20):
        try:
            if 'Route' not in self.df.columns:
                raise ValueError("Column 'Route' not found in DataFrame")
            route_count = self.df['Route'].value_counts().sort_values(ascending = False)
            top_route_counts = route_count.head(top_n)

            route_count_x= top_route_counts.index.tolist()
            route_count_y = top_route_counts.tolist()
            return route_count_x,route_count_y

        except (KeyError, ValueError) as e:
            print(f"Error occurred:{e}")
            return None
        except AttributeError as e:
            print(f'Attribute Error Occurred {e}')
            raise
            
        

    @handle_exceptions 
    def get_fatalities_by_route(self,top_n=20):
        try:
            route_fatalities = self.df.groupby ('Route')['Fatalities'].sum().nlargest(top_n)
            return route_fatalities
            
        except (KeyError, ValueError) as e:
            print(f"Error occurred:{e}")
            return None
        except AttributeError as e:
            print(f'Attribute Error Occurred {e}')
            raise
    
    

    @handle_exceptions
    def get_count(self, top_n=20):
        try:
            last_words = self.df['Location'].str.split().str[-1]
            countries_df = pd.DataFrame({'Region': last_words, 'count': np.ones(len(self.df))})
            countries_grouped = countries_df.groupby('Region').count().sort_values('count', ascending=False)
            return countries_grouped
        except (KeyError, ValueError) as e:
            print(f"Error occurred:{e}")
            return None
        except AttributeError as e:
            print(f"AttributeError occurred:{e}")
            raise
    
   
  
            

    def get_time_of_the_day(self, top_n=20):
        try:
            if self.df is None:
                raise ValueError("No data available")

            df = self.df.dropna(subset=['Time']).copy()
            df['Hour'] = df['Time'].astype(str).str[:2]
            df = df[df['Hour'].str.isnumeric()]

            if df.empty:
                raise ValueError("No valid data for time of the day")

            return df
        except Exception as e:
            print(f"Error in get_time_of_the_day: {e}")
            return None
        
    
    
                
    def visualization_operator(self, top_n=20):
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
            plt.savefig(os.path.join(self.df, plot_file))
            plt.clf()  # Clear the current figure
            
            return jsonify({'visualization_path': plot_file})
        
        except Exception as e:
            return jsonify({'error': str(e)})  
        
    def visualization_fatalities_by_route(self, top_n=20):
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
                plt.savefig(os.path.join(self.df, plot_file))
                plt.clf()  # Clear the current figure
                return jsonify({'visualization_path': plot_file})
        except Exception as e:
            return jsonify({'error': str(e)})
        
    def visualization_year(self, top_n=20):
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
            plt.savefig(os.path.join(self.df, plot_file))
            plt.clf()  # Clear the current figure
            return jsonify({'visualization_path': plot_file})
        except Exception as e:
            return jsonify({'error': str(e)})
        
    def visualization_fatalities_by_year(self, top_n=20):
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
            plt.savefig(os.path.join(self.df, plot_file))
            plt.clf()  # Clear the current figure
            
            return jsonify({'visualization_path': plot_file})

        except Exception as e:
            return jsonify({'error': str(e)})
    
    def visualization_count(self, top_n=20):
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
            plt.savefig(os.path.join(self.df, plot_file))
            plt.clf()  # Clear the current figure
            return jsonify({'visualization_path': plot_file})
        except Exception as e:
            return jsonify({'error': str(e)})
        
    def visualization_type_of_aircraft(self, top_n=20):
    
        try:
            global plot_counter
            type_count=self.df.groupby(['Type']).count().sort_values('index',ascending=False)
            tc_x=type_count.index
            tc_y=type_count['index']
            plt.ylabel('TYPE OF AIRCRAFT')
            plt.barh(tc_x[:20],tc_y[:20])
            plt.title(f'Top {top_n} Type Of Aircraft')
            plt.xlabel('Crashes')
        
            plot_counter += 1
            plot_file = f"route_visualization_{plot_counter}.png"

            # Save the plot with a unique filename
            plt.savefig(os.path.join(self.df, plot_file))
            plt.clf()  # Clear the current figure
            return jsonify({'visualization_path': plot_file})
        except Exception as e:
            return jsonify({'error': str(e)}) 
        
  
    def visualize_time_of_the_day(self, top_n=20):
        try:
            time_of_day_crashes = self.get_time_of_the_day(top_n=top_n)

            if time_of_day_crashes is not None:
                plt.bar(time_of_day_crashes['Hour'])
                plt.xlabel('Hour of the Day')
                plt.ylabel('Crash Count')
                plt.title('Crash Count by Time of Day')

                plot_file = 'time_of_the_day.png'
                plot_path = os.path.join(self.base_dir, plot_file)
                plt.savefig(plot_path)
                plt.close()

                return plot_file
            else:
                return jsonify({"error": "No data available"}), 404

        except Exception as e:
            print(f"Error in visualize_time_of_the_day: {e}")
            return jsonify({"error": str(e)}), 500
            
    
        
   


