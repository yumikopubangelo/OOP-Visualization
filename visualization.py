
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    def __init__(self, data_frame):
        """
        This function initializes the AirplaneCrashes class with a DataFrame.
        """
        self.df= data_frame

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
            op_fatalities = pd.DataFrame(self.df.groupby(['Operator']).sum()['Fatalities']).dropna(axis='rows')
            op_fatalities = op_fatalities.sort_values("Fatalities", ascending = False)
            op_fatalities_x = op_fatalities.index
            op_fatalities_y = op_fatalities ['Fatalities']
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
       
            plt.show()
        except AttributeError as e:
            print(f"AttributeError occurred:{e}")

    @handle_exceptions
    def get_route(self, top_n=20):
        try:
            route_counte = self.df.groupby (['Route']).count().sort_values (by='index', ascending=False)
            route_count_x =np.array(route_counte.index)
            route_count_y = np.array(route_counte['index'][:20])
            return route_count_x, route_count_y

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

            plt.show()
        except AttributeError as e:
            print(f'Attribute Error Occurred {e}')
        

    @handle_exceptions 
    def get_fatalities_by_route(self,top_n=20):
        try:
            route_fatalities = self.df.groupby (['Route']).sum().drop(['index','Ground'], axis = 'columns')
            route_fatalities = route_fatalities.sort_values ('Fatalities', ascending = False)
            route_fatalities[:20].plot(kind='barh')
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
                plt.xlabel('Passangers')    
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
            

    def get_count(self, top_n=20):
        try:
            locations = np.array(self.df['Location']).tolist()
            countries = []
            for loc in locations:
             countries.append(visualization_lastWord(loc))
      
            countries_df = pd.DataFrame({'Region': countries, 'count': np.ones(len(countries))})
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
    def get_type_of_aircraft(self, top_n):
        try:
            type_count=self.df.groupby(['Type']).count().sort_values('index', ascending = False)
            tc_x= type_count.index
            tc_y=type_count['index']
            return tc_x, tc_y
        except (KeyError, ValueError) as e:
            print(f"Error occurred:{e}")
            return None
        except AttributeError as e:
            print(f"AttributeError occurred:{e}")
            raise

    @handle_exceptions
    def visualization_type_of_aircraft(self, top_n=20):
        try:
            tc_y, tc_x = self.get_type_of_aircraft
            plt.barh(tc_x[:20],tc_y[:20])
            plt.ylabel(f'Top {top_n} Type Of Aircraft')
            plt.show()

        except AttributeError as e:
            print(f"AttributeError occurred:{e}")

  
    @handle_exceptions 
    def visualization_time_of_day(self,top_n=20):
        try:
            times_df = self.extract_hour()
            total_by_hour = times_df.groupby('Hour').count().sort_values('count', ascending=False)
            plt.barh(total_by_hour[:20].index, total_by_hour[:20]['count'][:top_n])
            plt.ylabel('Hour')
            plt.xlabel('Crashes')
            plt.title(f'Top {top_n} Hours in Airplane Crashes')
            plt.show()

        except (KeyError, ValueError,AttributeError) as e:
            print(f"Error occurred:{e}")
            

    @handle_exceptions
    def get_time_of_the_day(self, top_n=20):
        try:
            df=self.df.dropna(subset=['Time']).copy()
            df['Hour'] = df['Time'].astype(str).str[:2]
            df=df[df['Hour'].str.isnumeric()]
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

     
    


file_path= r"C:\Users\vanguard\OneDrive\Documents\GitHub\OOP-Visualization\AirplaneCrashes.csv"
df = pd.read_csv(file_path)

visualizer = AirplaneCrashes(df)

try:
    visualizer.visualization_top_operator(top_n=20)
    visualizer.visualization_operator(top_n=20) 
    visualizer.visualization_route(top_n=20)
    visualizer.visualization_fatalities_by_route(top_n=20) 
    visualizer.visualization_year( top_n=20)
    visualizer.visualization_fatalities_by_year(top_n=20)
    visualizer.visualization_count(top_n=20)
    visualizer.visualization_type_of_aircraft(top_n=20)
    visualizer.visualization_time_of_day(top_n=20)
    visualizer.visualization_time_of_the_day(top_n=20)

except Exception as e:
    print(f"Error occurred: {e}")

#
#This code provides a class called `AirplaneCrashes` that allows you to visualize various aspects of airplane crashes. The class has several methods, each of which generates a different visualization. The visualizations include the top operators accounting for crashes, the top operators in terms of fatalities, the top routes in terms of crashes, fatalities by route, the distribution of crashes by year, fatalities and the number of individuals aboard per year, and the count of crashes by region.
#
