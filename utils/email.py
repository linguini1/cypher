# Imports
import smtplib
import ssl

# Constants

PORT = 465  # SSL
CONTEXT = ssl.create_default_context()


# Functions
def sms_email(number: str) -> str:

    """Returns the email address for the SMS number."""

    return f"{number}@msg.telus.com"


def create_message(subject: str | None, body: str) -> str:

    """Returns formatted message so that subject appears properly in email."""

    if subject:
        return f"{subject}\n\n{body}"
    else:
        return body


def send_email(to: str, from_: str, message: str, password: str, is_text=False):

    """Sends email to recipient address."""

    # Convert number to email address
    if is_text:
        to = sms_email(to)

    # Starting up connections
    with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=CONTEXT) as server:
        server.login(from_, password)

        # Send email
        server.sendmail(
            from_,
            to,
            message
        )


def cypher_credentials() -> tuple[str, str]:

    """Gets the credentials for the cypher.py email."""

    with open("./resources/email.txt", "r") as file:

        email = next(file)
        password = next(file)

    return email, password
