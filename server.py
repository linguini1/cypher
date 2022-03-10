# Imports
from flask import Flask, request
from parsers import RequestParser
from handlers import MainHandler
from pprint import pprint

# Create API
app = Flask(__name__)


# API submission route
@app.route('/submit', methods=['POST'])
def submit():

    # Parse data
    data = request.get_json()
    pprint(data)
    parser = RequestParser(data)

    # Handle event
    event_handler = MainHandler(parser)  # Instantiate handler
    response = event_handler.get_handler()  # Handle event

    pprint(response.json_response)

    return response.json_response  # Send response


# Run API on port 80
if __name__ == '__main__':
    app.run(port=80)
