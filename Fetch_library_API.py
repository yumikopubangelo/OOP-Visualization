import requests 

def fetch_libraries(query):
    url = f"https://pypi.org/pypi/numpy/json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print (f"Failed to fetch data. status code : {response.status_code}")

# Example usage
library_name = 'requests'
library_data = fetch_libraries (library_name)

if library_data:
    print (f"Infromation about {library_name}:")
    print (library_data)