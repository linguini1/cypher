# Utility functions
__author__ = "Matteo Golin"

# Imports
from .email import create_message, send_email, cypher_credentials

# Constants


# Functions
def dispatch(to: str, subject: str = None, body: str = None, is_text: bool = False):

    """Sends the specified email to the specified recipient."""

    # Format message for text or email
    if is_text:
        message = subject
    else:
        message = create_message(subject, body)

    # Get mailer credentials
    usr, pswd = cypher_credentials()

    # Send email
    send_email(
        to,
        from_=usr,
        message=message,
        password=pswd,
        is_text=is_text
    )