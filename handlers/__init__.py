# Event handler classes
__author__ = "Matteo Golin"

# Imports
from inspect import getmembers, ismethod
import json
import response as r

# Constants


# Base event handler
class EventHandler:

    def __init__(self, parser):

        # Main parser
        self.parser = parser

        # Quick access
        self.session_id = self.parser.session.id_

        # Load important data
        with open("resources/data.json") as file:
            self.program_data = json.load(file)

        # Load application credentials
        with open("resources/credentials.json") as file:
            self.credentials = json.load(file)

        # Basic suggestions
        self.yes = r.Suggestion("Yes")
        self.no = r.Suggestion("Nope")
        self.nevermind = r.Suggestion("Nevermind")
        self.action_prompts = [
            r.Suggestion("Complete CU Screen"),
            r.Suggestion("Get headlines")
        ]

    def handle_event(self):

        """
        Selects the method matching the passed event and calls it with the event parameters.
        Returns a unique WebhookResponse object with the data populated by the called method.
        """

        event_handler = getattr(self, self.parser.handler.name)
        return event_handler()


# Event handlers
class SpeechResponseHandler(EventHandler):

    """Will handle simple responses within the application."""

    def __init__(self, parser):
        super().__init__(parser)

    def invocation(self):

        """Response on main invocation."""

        response_value = "Cypher at your service."

        response = r.SimpleResponse(
            text=response_value,
            speech=response_value
        )

        webhook_response = r.WebhookResponse(
            session_id=self.session_id,
            simples=[response],
        )

        return webhook_response

    def start(self):

        """Start scene with some prompts for common use-cases."""

        # Create reply
        question = "What can I do for you?"

        response = r.SimpleResponse(
            text=question,
            speech=question,
        )

        # Create webhook response
        webhook_response = r.WebhookResponse(
            session_id=self.session_id,
            simples=[response],
            suggestions=self.action_prompts  # Common actions
        )

        return webhook_response

    def reprompt(self):

        """Reprompts the user."""

        # Create reply
        question = "Anything else I can do?"

        response = r.SimpleResponse(
            text=question,
            speech=question,
        )

        # Create webhook response
        webhook_response = r.WebhookResponse(
            session_id=self.session_id,
            simples=[response],
            suggestions=self.action_prompts + [self.no]  # Common actions
        )

        return webhook_response


# Selector
class MainHandler(EventHandler):

    def __init__(self, parser):
        super().__init__(parser)

        # Define all event handlers
        self.event_handlers = [
            SpeechResponseHandler,
        ]

    def get_handler(self):

        """
        Selects the appropriate event handler for the event, and returns the handle_event function call,
        which selects the appropriate method from the selected handler to handle the passed event.

        Ultimately returns a WebhookResponse.
        """

        # Find the event handler with a method matching the event
        for handler in self.event_handlers:

            # Instantiate handler
            event_handler = handler(self.parser)

            # Get all events handled by given handler
            events = [event for event, value in getmembers(event_handler, predicate=ismethod)]

            # Handle the event if the correct handler is found
            if self.parser.handler.name in events:
                return event_handler.handle_event()

        return None  # No handler found
