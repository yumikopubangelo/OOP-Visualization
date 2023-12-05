
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from functools import wraps


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


    

class AirplaneCrashes:
    def __init__(self, data_frame, base_dir):
        """
        This function initializes the AirplaneCrashes class with a DataFrame.
        """
        self.df= data_frame

        self.base_directory = base_dir

            

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
    def visualization_top_operator(self , top_n=20):
        """
        This function visualizes the top operators accounting for crashes.
        """
        try:
            top_operators = self.get_top_operator(top_n)            
            plt.figure(figsize=(40,8))
            top_operators.plot(kind = 'barh')
            plt.xlabel('Crashes')
            plt.ylabel('Top Operator')
            plt.title(f'Top {top_n} Operator Accounting For Crashes')
       
            plt.show()

      
        except Exception as e:
            print(f"Error:{e}")

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
       
            plt.show()
        except AttributeError as e:
            print(f"AttributeError occurred:{e}")

    @handle_exceptions
    def get_route(self, top_n=20):
        try:
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

            plt.show()
        except AttributeError as e:
            print(f'Attribute Error Occurred {e}')
        

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
                plt.show()
        except AttributeError as e:
            print(f'Attribute Error Occurred {e}')


    @handle_exceptions
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

            plt.show()

        except (KeyError, ValueError,AttributeError) as e:
            print(f"Error occurred:{e}")

    @handle_exceptions
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
            plt.show()

        except (KeyError, ValueError,AttributeError) as e:
            print(f"Error occurred:{e}")
            

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
            plt.show()

        
        except AttributeError as e:
            print(f"AttributeError occurred:{e}")

    @handle_exceptions
    def visualization_type_of_aircraft(self, top_n=20):
        try:
            type_count=df.groupby(['Type']).count().sort_values('index',ascending=False)
            tc_x=type_count.index
            tc_y=type_count['index']
            plt.ylabel('TYPE OF AIRCRAFT')
            plt.barh(tc_x[:20],tc_y[:20])
            plt.title(f'Top {top_n} Type Of Aircraft')
            plt.xlabel('Crashes')
        except (KeyError, ValueError) as e:
            print(f"Error occurred:{e}")
            return None
        except AttributeError as e:
            print(f"AttributeError occurred:{e}")
            raise

  
            

    @handle_exceptions
    def get_time_of_the_day(self, top_n=20):

        try:
            df = self.df.dropna(subset=['Time']).copy()
            df['Hour'] = df['Time'].astype(str).str[:2]
            df = df[df['Hour'].str.isnumeric()]
            df['Hour'] = df['Hour'].astype(int)
            return df
        except (KeyError, ValueError) as e:
                print(f"Error occurred:{e}")
                return None
        except AttributeError as e:
            print(f"AttributeError occurred:{e}")
            raise


    @handle_exceptions
    def visualization_time_of_the_day(self, top_n=20):
        try:
            time_count= self.get_time_of_the_day()

            if time_count is not None:      
                time_count= time_count['Hour'].value_counts().sort_index()
                time_count.plot(kind='bar')
                plt.xlabel('Hour of the Day')
                plt.ylabel('Crash Count')
                plt.title('Crashes by Time of Day')
                plt.show()

        except AttributeError as e:
            print(f"AttributeError occurred:{e}")

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


visualizer = AirplaneCrashes(df, base_directory)

try:
    visualizer.visualization_operator(top_n=20) 
    visualizer.visualization_top_operator(top_n=20)
    visualizer.visualization_time_of_the_day(top_n=20)
    visualizer.visualization_count(top_n=20)
    visualizer.visualization_route(top_n=20)
    visualizer.visualization_type_of_aircraft(top_n=20)
    visualizer.visualization_fatalities_by_route(top_n=20) 
    visualizer.visualization_year( top_n=20)
    visualizer.visualization_fatalities_by_year(top_n=20)

except Exception as e:
    print(f"Error occurred: {e}")

#
#This code provides a class called `AirplaneCrashes` that allows you to visualize various aspects of airplane crashes. The class has several methods, each of which generates a different visualization. The visualizations include the top operators accounting for crashes, the top operators in terms of fatalities, the top routes in terms of crashes, fatalities by route, the distribution of crashes by year, fatalities and the number of individuals aboard per year, and the count of crashes by region.
#
