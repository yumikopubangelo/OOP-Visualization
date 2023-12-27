from flask import Flask, jsonify
from route import setup_routes
from visualization import AirplaneCrashes

app = Flask(__name__)


visualizer = AirplaneCrashes()


# Call setup_routes function to map routes to functions
setup_routes(app, visualizer)

if __name__ == '__main__':
    app.run(debug=True)
