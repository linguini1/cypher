# Imports

# Classes
class Image:

    def __init__(self, url: str, alt: str, width=0, height=0):
        self.url = url
        self.alt = alt
        self.width = width
        self.height = height

    @property
    def json_response(self):

        representation = {
            "alt": self.alt,
            "height": self.height,
            "width": self.width,
            "url": self.url,
        }

        return representation


class Button:

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url

    @property
    def json_response(self):

        representation = {
            "name": self.name,
            "open": {
                "url": self.url,
                "hint": "HINT_UNSPECIFIED"
            }
        }

        return representation


class Card:

    def __init__(self, title: str, subtitle: str, text: str, image=None, button=None):
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.image = image
        self.button = button

    @property
    def json_response(self):

        representation = {
            "title": self.title,
            "subtitle": self.subtitle,
            "text": self.text,
        }

        # Adding image
        if self.image:
            representation["image"] = self.image.json_response

        # Adding button
        if self.button:
            representation["button"] = self.image.json_response

        return representation


class SimpleResponse:

    def __init__(self, text: str, speech: str, first=True):
        self.name = "firstSimple" if first else "lastSimple"  # If the response is first or last (first by default)
        self.text = text
        self.speech = speech

    @property
    def json_response(self):

        representation = {
            self.name: {
                "text": self.text,
                "speech": self.speech,
            }
        }

        return representation


class Suggestion:

    def __init__(self, title: str):
        self.title = title

    @property
    def json_response(self):

        representation = {
            "title": self.title,
        }

        return representation


class ListItem:

    def __init__(self, key: int, title: str, description: str, image: Image | None = None):
        self.key = key
        self.title = title
        self.description = description
        self.image = image

    @property
    def json_response(self):

        representation = {
            "key": self.key,
            "title": self.title,
            "description": self.description,
        }

        if self.image:
            representation.update({"image": self.image.json_response})

        return representation


class List:

    def __init__(self, title: str, subtitle: str, items: list[ListItem]):
        self.title = title
        self.subtitle = subtitle
        self.items = items

    @property
    def json_response(self):

        representation = {
            "title": self.title,
            "subtitle": self.subtitle,
            "items": [{"key": f"ITEM_{item.json_response['key'] + 1}"} for item in self.items]
        }

        return representation


class WebhookResponse:

    def __init__(
            self,
            session_id: str,
            params: dict | None,
            simples: list | None = None,
            suggestions: list | None = None,
            card: Card | None = None,
            list_: List | None = None,
    ):

        self.session_id = session_id
        self.params = params if params else {}
        self.simples = simples if simples else []  # Empty array if no simple responses are passed
        self.suggestions = suggestions if suggestions else []  # Empty array if no suggestions are specified
        self.card = card
        self.list = list_

    @property
    def json_response(self):

        representation = {
            "session": {
                "id": self.session_id,
                "params": self.params
            },
            "prompt": {
                "override": False,
            }
        }

        # Adding simple responses
        for simple in self.simples:
            representation["prompt"].update(simple.json_response)

        # Adding suggestions
        representation["prompt"]["suggestions"] = [suggestion.json_response for suggestion in self.suggestions]

        # Adding card content
        if self.card:
            representation["prompt"]["content"] = {"card": self.card.json_response}

        # Adding list
        if self.list:
            representation["prompt"]["content"] = {"list": self.list.json_response}
            representation["prompt"]["override"] = False

            representation["session"]["typeOverrides"] = [{
                "name": "prompt_option",
                "synonym": {
                    "entries": []
                },
                "typeOverrideMode": "TYPE_REPLACE"
            }]

            entries_list = representation["session"]["typeOverrides"][0]["synonym"]["entries"]

            for item in self.list.items:

                altered_item = item.json_response.copy()
                altered_item.pop("key")

                entries_list.append(
                    {
                        "name": f"ITEM_{item.json_response['key'] + 1}",
                        "synonyms": [f"Item {item.json_response['key'] + 1}"],
                        "display": altered_item
                    }
                )

        return representation
