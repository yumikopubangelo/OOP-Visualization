
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
    def __init__(self, df=None, base_dir='C:\\Users\\vanguard\\OneDrive\\Documents\\GitHub\\OOP-Visualization'):
        """
        This function initializes the AirplaneCrashes class with a DataFrame and base directory.
        """
        self.base_directory = base_dir  # Assign the provided base directory to the object's attribute or use the default value
        if df is None:
            self.df = self.read_sanitized_csv('C:\\Users\\vanguard\\OneDrive\\Documents\\GitHub\\OOP-Visualization\\AirplaneCrashes.csv')  # Replace 'path_to_your_data.csv' with your actual data file
        else:
            self.df = df  # Assign the provided DataFrame to self.df if provided or read CSV if None

    def read_sanitized_csv(self, file_path):
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return None
        


            

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
    def read_sanitized_csv(self, file_path):
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return None
    def check_df_type(self):
        print(type(self.df))
        return type(self.df)
