import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class AirplaneCrashes:
    def __init__(self, data_frame):
        self.df= data_frame
        

    def visualization_top_operator(self , top_n=20):
        operator_count = self.df.groupby(['Operator']).count()['index']
        operator_count = pd.DataFrame(operator_count).dropna(axis='rows')
        operator_count = operator_count.rename (columns={'index' : 'count'})
        operator_count = operator_count.sort_values("count", ascending=False)
        
        op_count_x = operator_count.index[:top_n]
        op_count_y = operator_count['count'][:top_n]

        plt.figure(figsize=(40,8))
        plt.barh (op_count_x, op_count_y)
        plt.xlabel('Crashes')
        plt.ylabel('Top Operator')
        plt.title(f'Top {top_n} Operator Accounting For Crashes')
        
        plt.show()


    def visualization_operator(self, top_n=20):
        op_fatalities = pd.DataFrame(self.df.groupby(['Operator']).sum()['Fatalities'])
        op_fatalities = op_fatalities.sort_values("Fatalities", ascending = False)
        op_fatalities_x = op_fatalities.index
        op_fatalities_y = op_fatalities ['Fatalities']

        plt.figure(figsize=(30,20))
        plt.barh (op_fatalities_x[:20], op_fatalities_y[:20])
        plt.xlabel ('Fatalities')
        

        plt.show()

    def visualization_route(self, top_n=20):
        route_counte = self.df.groupby (['Route']).count().sort_values (by='index', ascending=False)
        route_count_x =np.array(route_counte.index)
        route_count_y = np.array(route_counte['index'])
        plt.figure(figsize=(30,20))
        plt.barh (route_count_x[:20], route_count_y[:20])
        plt.xlabel ('Crashes')

        plt.show()

    def visualization_fatalities_by_route(self, top_n=20):
        route_fatalities = self.df.groupby (['Route']).sum().drop(['index','Ground'], axis = 'columns')
        route_fatalities = route_fatalities.sort_values ('Fatalities', ascending = False)
        route_fatalities[:20].plot(kind='barh')
        plt.xlabel('Passangers')

        plt.show()

    def visualization_year(self, top_n=20):
        years = pd.to_datetime(self.df['Date']).dt.year
        year_count = years.value_counts().head(top_n).sort_values(ascending=False)

        plt.figure(figsize=(10, 6))
        sns.histplot(years, kde=True, color='green')
        plt.xlabel('Year')
        plt.title(f'Top {top_n} Year Distribution')

        plt.show()
  
    



file_path=  r"C:\Users\vanguard\OneDrive\Documents\GitHub\OOP-Visualization\AirplaneCrashes.csv"
df = pd.read_csv(file_path)

visualizer = AirplaneCrashes(df)

visualizer.visualization_top_operator(top_n=20)
visualizer.visualization_operator(top_n=20)
visualizer.visualization_route(top_n=20)
visualizer.visualization_fatalities_by_route(top_n=20) 
visualizer.visualization_year( top_n=20)
visualizer.visualization_year(top_n=20)