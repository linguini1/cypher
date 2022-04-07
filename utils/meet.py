# Google meet functions

# Constants
BASE_URL = "https://meet.google.com/"
MEET_ALERT_SUBJECT = "Hey! Join the meet!"
DEFAULT_CODE = "rrc-uaqo-vyt"


# Functions
def is_hyphenated(code: str) -> bool:

    """Checks if the code is already in hyphenated form."""

    return "-" in code


def format_meet_url(code: str) -> str:

    """Returns the meet URL."""

    if not is_hyphenated(code):
        code = f"{code[:3]}-{code[3:7]}-{code[7:]}"

    return f"{BASE_URL}{code}"


def meet_alert_body(url: str) -> str:

    body = f"You're personally invited to Matteo's Google Meet, taking place... NOW!" \
           f"You can find the link here: {url}" \
           f"See you soon!"

    return body
