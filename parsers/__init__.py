# Parser class for making requesst data more easily accessible
__author__ = "Matteo Golin"

# Imports
from pprint import pprint
from dataclasses import dataclass

# Constants


# Classes
@dataclass
class Device:
    capabilities: list[str]
    time_zone: str


@dataclass
class Handler:
    name: str


@dataclass
class Home:
    params: dict[str, str]


@dataclass
class Intent:
    name: str
    params: dict[str, str]
    query: str


@dataclass
class Scene:
    name: str
    next: str
    slot_filling_status: str
    slots: dict[str, str]


@dataclass
class Session:
    id_: str
    language_code: str
    params: dict[str, str]
    type_overrides: list


@dataclass
class User:
    account_linking_status: str
    gaiamint: str
    last_seen_time: str
    locale: str
    package_entitlements: list
    params: dict[str, str]
    permissions: list
    verification_status: str


class RequestParser:

    """Parses the request into an object for easy data accessibility."""

    def __init__(self, request_data: dict):

        pprint(request_data)
        self._raw_data = request_data

        self.device = Device(
            request_data["device"]["capabilities"],
            request_data["device"]["timeZone"]["id"]
        )

        self.handler = Handler(
            request_data["handler"]["name"]
        )

        self.home = Home(
            request_data["home"]["params"]
        )

        self.intent = Intent(
            request_data["intent"]["name"],
            request_data["intent"]["params"],
            request_data["intent"]["query"]
        )

        self.scene = Scene(
            request_data["scene"]["name"],
            request_data["scene"].get("next"),
            request_data["scene"]["slotFillingStatus"],
            request_data["scene"]["slots"]
        )

        self.session = Session(
            request_data["session"]["id"],
            request_data["session"]["languageCode"],
            request_data["session"]["params"],
            request_data["session"]["typeOverrides"]
        )

        self.user = User(
            request_data["user"]["accountLinkingStatus"],
            request_data["user"]["gaiamint"],
            request_data["user"]["lastSeenTime"],
            request_data["user"]["locale"],
            request_data["user"]["packageEntitlements"],
            request_data["user"]["params"],
            request_data["user"]["permissions"],
            request_data["user"]["verificationStatus"]
        )
