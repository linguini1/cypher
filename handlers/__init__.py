# Imports
from inspect import getmembers, ismethod
import threading
import utils as f
import response as r


# Base event handler
class EventHandler:

    def __init__(self, parser):

        # Main parser
        self.parser = parser

        # Quick access
        self.session_id = self.parser.session.id

        # My sms number for notifications
        with open("resources/sms.txt", "r") as file:
            self.sms = next(file)

        # Basic suggestions
        self.yes = r.Suggestion("Yes")
        self.no = r.Suggestion("No")
        self.nevermind = r.Suggestion("Nevermind")
        self.action_prompts = [
            r.Suggestion("Complete CU Screen")
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
            suggestions=self.action_prompts + [self.nevermind]  # Common actions
        )

        return webhook_response


class SchoolHandler(EventHandler):

    def __init__(self, parser):
        super().__init__(parser)

    def say_hi(self):

        """Test event handler, no practical use."""

        num_hi = self.parser.session.params["num_hi"]

        # Logic
        if num_hi > 0:
            hi_string = f"{'hi ' * num_hi}"
            card = r.Card(
                title="Greetings",
                subtitle="This is how many times you wanted to say hi:",
                text=hi_string
            )

        else:  # Error handling
            hi_string = "I can't say hi less than 0 times!"
            card = None

        # Create simple response
        simple_response = r.SimpleResponse(
            first=True,
            text=hi_string,
            speech=hi_string
        )

        # Create webhook response
        webhook_resp = r.WebhookResponse(
            session_id=self.session_id,
            simples=[simple_response],
            card=card
        )

        return webhook_resp

    def cuScreen(self):

        """Fills out cuScreen self-assessment."""

        def executable():

            with open("resources/cuScreenCreds.txt", "r") as file:
                usr = next(file)
                pswd = next(file)

            f.complete_self_assessment(usr, pswd)
            f.dispatch(self.sms, "Self assessment completed.", is_text=True)  # Notify when complete

        threading.Thread(target=executable).start()  # Run the function and let the response go out

        success = "Your assessment should be done in a few seconds."

        response = r.SimpleResponse(
            text=success,
            speech=success,
        )

        webhook_response = r.WebhookResponse(
            session_id=self.session_id,
            simples=[response]
        )

        return webhook_response


class BasicsHandler(EventHandler):

    def __init__(self, parser):
        super().__init__(parser)

    def confirm_email(self):

        """Confirms email fields to user before sending."""

        # Unpack params
        params = self.parser.session.params
        email = params["email"]
        subject = params.get("subject")
        body = params["body"]

        # Verification depends if there is a subject line
        if subject:
            confirm_subject = f" with subject line {subject}"
        else:
            confirm_subject = ""

        # Create response
        email_speech = f"You want to send an email that says {body} to {email}{confirm_subject}."
        read_email = r.SimpleResponse(
            text=email_speech,
            speech=email_speech,
        )

        verify = "Is that correct?"
        verification = r.SimpleResponse(
            text=verify,
            speech=verify,
            first=False  # Read last
        )

        # Email visual representation
        email_card = r.Card(
            title=f"Your email to {email}",
            subtitle=subject,
            text=body,
        )

        # Send response
        webhook_response = r.WebhookResponse(
            session_id=self.session_id,
            simples=[read_email, verification],
            card=email_card,
            suggestions=[self.yes, self.no]
        )

        return webhook_response

    def send_email(self):

        """Sends an email with the specified message to the specified address."""

        # Unpack params
        params = self.parser.session.params
        email = params["email"]
        subject = params.get("subject")
        body = params["body"]

        # Send email
        f.dispatch(
            to=email,
            subject=subject,
            body=body
        )

        # Create response
        success = "Your email has been sent to the server."
        confirmation = r.SimpleResponse(
            text=success,
            speech=success,
        )

        # Card for email display.
        email_card = r.Card(
            title=f"Your email to {email}",
            subtitle=subject,
            text=body,
        )

        # Return response
        webhook_response = r.WebhookResponse(
            session_id=self.session_id,
            simples=[confirmation],
            card=email_card
        )

        return webhook_response

    def get_headlines(self):

        """Gets the latest headlines."""

        # Unpacking parameters
        params = self.parser.session.params
        category = params.get("category")
        key_word = params.get("key_word")
        country = params.get("country")

        # Getting articles
        api_request = f.create_url(category, key_word, country)
        articles = f.get_articles(api_request)
        headlines = f.get_titles(articles)

        # Responding

        # Context
        intro_text = "Here are the top 6 headlines."
        intro = r.SimpleResponse(
            text=intro_text,
            speech=intro_text
        )

        # Headlines
        headline_text = ""
        for _ in range(len(headlines)):
            headline_text += f"Headline Number {_ + 1}: {headlines[_]}."

        headline_response = r.SimpleResponse(
            text=headline_text,
            speech=headline_text,
            first=False
        )

        # Articles
        article_list = []
        for _ in range(len(articles)):

            article = articles[_]

            image = r.Image(
                url=article["urlToImage"],
                alt="Article image"
            )

            article_item = r.ListItem(
                key=f"#{_}",
                title=article["title"],
                description=article["description"],
                image=image
            )

            article_list.append(article_item)

        list_response = r.List(
            title="Headlines",
            subtitle=f"Top headlines for today in {country}.",
            items=article_list
        )

        # Return response
        webhook_response = r.WebhookResponse(
            session_id=self.session_id,
            simples=[headline_response],
            list_=list_response
        )

        return webhook_response


# Selector
class MainHandler(EventHandler):

    def __init__(self, parser):
        super().__init__(parser)

        # Define all event handlers
        self.event_handlers = [
            SpeechResponseHandler,
            SchoolHandler,
            BasicsHandler,
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

            print(self.parser.handler.name)

            # Handle the event if the correct handler is found
            if self.parser.handler.name in events:
                return event_handler.handle_event()

        return None  # No handler found
