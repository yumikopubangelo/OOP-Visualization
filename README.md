# OOP-Visualization
def read_sanitized_csv(user_input):
        file_path = sanitize_path(user_input)
        df = pd.read_csv(file_path)
        return df

    sanitized_path = sanitize_path('AirplaneCrashes.csv')
    df = read_sanitized_csv('AirplaneCrashes.csv')

    user_input = "C:\Users\vanguard\OneDrive\Documents\GitHub\OOP-Visualization\AirplaneCrashes.csv"
    try:
        sanitized_path = sanitize_path(user_input)
        df = read_sanitized_csv(user_input)
        with open(sanitized_path, 'r') as file:
            pass
    except ValueError as e:
        print(f"Error: {e}")

        "C:\Users\vanguard\OneDrive\Documents\GitHub\OOP-Visualization\OOP-Visualization"