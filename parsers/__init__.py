# Imports

# Classes
class RequestParser:

    def __init__(self, request_data: dict):

        # Convert all request data into an accessible namespace
        for key, value in request_data.items():

            # I want params as a dict because .get() is convenient
            if type(value) == dict and key != "params":
                request_data[key] = RequestParser(value)

        self.__dict__.update(request_data)
