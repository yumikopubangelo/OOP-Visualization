
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

def crash_times(crash_datetime):
   times = crash_datetime.dt.strftime('%H')
   return times

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
    def visualization_top_operator(self , top_n=20):
        """
        This function visualizes the top operators accounting for crashes.
        """
        try:
            if 'Operator' not in self.df.columns:
                raise ValueError("column 'Operator' not found in DataFrame")
            
            operator_counts = self.df['Operator'].value_counts().dropna()
            top_operators = operator_counts.head(top_n)

            plt.figure(figsize=(40,8))
            top_operators.plot(kind = 'barh')
            plt.xlabel('Crashes')
            plt.ylabel('Top Operator')
            plt.title(f'Top {top_n} Operator Accounting For Crashes')
        
            plt.show()

       
        except Exception as e:
            print(f"Error:{e}")

    @handle_exceptions
    def visualization_operator(self, top_n=20):
        """
        This function visualizes the top operators in terms of fatalities.
        """
        try:
        
            op_fatalities = pd.DataFrame(self.df.groupby(['Operator']).sum()['Fatalities']).dropna(axis='rows')
            op_fatalities = op_fatalities.sort_values("Fatalities", ascending = False)
            op_fatalities_x = op_fatalities.index
            op_fatalities_y = op_fatalities ['Fatalities']

            plt.figure(figsize=(30,20))
            plt.barh (op_fatalities_x[:20], op_fatalities_y[:20])
            plt.xlabel ('Fatalities')
        
            plt.show()
        except KeyError as e:
            print(f"KeyError occurred:{e}")
        except ValueError as e:
            print(f"ValueError occurred:{e}")

    @handle_exceptions
    def visualization_route(self, top_n=20):
        """
        This function visualizes the top routes in terms of crashes.
        """
        try:
            route_counte = self.df.groupby (['Route']).count().sort_values (by='index', ascending=False)
            route_count_x =np.array(route_counte.index)
            route_count_y = np.array(route_counte['index'])
            plt.figure(figsize=(30,20))
            plt.barh (route_count_x[:20], route_count_y[:20])
            plt.xlabel ('Crashes')

            plt.show()
        except KeyError as e:
            print(f"KeyError occurred:{e}")
        except ValueError as e:
            print(f"ValueError occurred:{e}")

    @handle_exceptions
    def visualization_fatalities_by_route(self, top_n=20):
        """
        This function visualizes the fatalities by route.
        """
        try:
            route_fatalities = self.df.groupby (['Route']).sum().drop(['index','Ground'], axis = 'columns')
            route_fatalities = route_fatalities.sort_values ('Fatalities', ascending = False)
            route_fatalities[:20].plot(kind='barh')
            plt.xlabel('Passangers')

            plt.show()
        except KeyError as e:
            print(f"KeyError occurred:{e}")
        except ValueError as e:
            print(f"ValueError occurred:{e}")

    @handle_exceptions
    def visualization_year(self, top_n=20):
        """
        This function visualizes the distribution of crashes by year.
        """
        years = pd.to_datetime(self.df['Date']).dt.year
        year_count = years.value_counts().head(top_n).sort_values(ascending=False)

        plt.figure(figsize=(10, 6))
        sns.histplot(years, kde=True, color='green')
        plt.xlabel('Year')
        plt.title(f'Top {top_n} Year Distribution')

        plt.show()

    @handle_exceptions
    def visualization_fatalities_by_year(self, top_n=20):
        """
        This function visualizes the fatalities and number of individuals aboard per year.
        """
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

     
    @handle_exceptions 
    def visualization_count(self, top_n=20):
        """
        This function visualizes the count of crashes by region.
        """
        locations = np.array(self.df['Location']).tolist()
        countries = []
        for loc in locations:
            countries.append(visualization_lastWord(loc))
       
        countries_df = pd.DataFrame({'Region': countries, 'count': np.ones(len(countries))})
        countries_grouped = countries_df.groupby('Region').count().sort_values('count', ascending=False)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x=countries_grouped['count'][:top_n], y=countries_grouped.index[:top_n])
        plt.xlabel('Count')
        plt.ylabel('Region')
        plt.title(f'Top {top_n} Regions in Airplane Crashes')
        plt.show()

    @handle_exceptions
    def visualization_type_of_aircraft(self, top_n=20):
        type_count=self.df.groupby(['Type']).count().sort_values('index', ascending = False)
        tc_x= type_count.index
        tc_y=type_count['index']
        plt.barh(tc_x[:20],tc_y[:20])
        plt.ylabel(f'Top {top_n} Type Of Aircraft')
        plt.show()

   
    @handle_exceptions
    def extract_hour(self):
        time_df = pd.DataFrame(self.df.groupby(['Time']).count().sort_values('index', ascending=False)['index'])
        times = np.array(time_df.index)
        crash_times = []
        for i in range(len(times)):
            if times[i][0] == 'c':
                times[i] = times[i][3:5]
            else:
                times[i] = times[i][:2]
                crash_times.append(times[i][:2])

        times_df = pd.DataFrame({'Hour': crash_times, 'count': np.ones(len(crash_times))})
        return times_df
    
    @handle_exceptions  
    def visualization_time_of_day(self,top_n=20):
        times_df = self.extract_hour()
        total_by_hour = times_df.groupby('Hour').count().sort_values('count', ascending=False)
        plt.barh(total_by_hour[:20].index, total_by_hour[:20]['count'])
        plt.ylabel('Hour')
        plt.xlabel('Crashes')
        plt.show()

    @handle_exceptions
    def visualization_time_of_the_day(self, top_n=20):
        df=self.df.dropna(subset=['Time'])
        df['Hour'] = df['Time'].astype(str).str[:2]
        df=df[df['Hour'].str.isnumeric()]
        df['Hour'] = df['Hour'].astype(int)

        time_count= df['Hour'].value_counts().sort_index()
        time_count.plot(kind='bar')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Crash Count')
        plt.title('Crashes by Time of Day')
        plt.show()

      
     


file_path= r"C:\Users\vanguard\OneDrive\Documents\GitHub\OOP-Visualization\AirplaneCrashes.csv"
df = pd.read_csv(file_path)

visualizer = AirplaneCrashes(df)


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

#
#This code provides a class called `AirplaneCrashes` that allows you to visualize various aspects of airplane crashes. The class has several methods, each of which generates a different visualization. The visualizations include the top operators accounting for crashes, the top operators in terms of fatalities, the top routes in terms of crashes, fatalities by route, the distribution of crashes by year, fatalities and the number of individuals aboard per year, and the count of crashes by region.