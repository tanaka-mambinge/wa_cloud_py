from enum import Enum
from typing import Union


class MessageType(str, Enum):
    ORDER = "order"
    TEXT = "text"
    INTERACTIVE = "interactive"
    IMAGE = "image"
    LOCATION = "location"
    REACTION = "reaction"
    VIDEO = "video"


class User:
    def __init__(self, data: dict):
        self.name: str = data.get("profile", {}).get("name", None)
        self.phone_number: str = data.get("wa_id", None)

    def __repr__(self):
        return f"User(name={self.name}, phone_number={self.phone_number})"


class InteractiveMessage:
    def __init__(self, data: dict, user: User):
        self.id: str = data.get("id", None)
        self.user: User = user
        self.context_message_id: str = data.get("context", {}).get("id", None)
        self.timestamp: str = data.get("timestamp", None)
        self.type: str = data.get("type", None)
        self.reply_id: str = (
            data.get("interactive", {}).get("list_reply", {}).get("id", None)
        )
        self.title: str = (
            data.get("interactive", {}).get("list_reply", {}).get("title", None)
        )
        self.description: str = (
            data.get("interactive", {}).get("list_reply", {}).get("description", None)
        )

    def __repr__(self):
        return f"InteractiveMessage(id={self.id}, timestamp={self.timestamp}, reply_id={self.reply_id}, title={self.title}, description={self.description}, user={self.user})"


class TextMessage:
    def __init__(self, data: dict, user: User):
        self.id: str = data.get("id", None)
        self.user: User = user
        self.context_message_id: str = data.get("context", {}).get("id", None)
        self.timestamp: str = data.get("timestamp", None)
        self.type: str = data.get("type", None)
        self.body: str = data.get("text", {}).get("body", None)

    def __repr__(self):
        return f"TextMessage(id={self.id}, timestamp={self.timestamp}, type={self.type}, body={self.body}, user={self.user})"


class Product:
    def __init__(self, data: dict):
        self.id: str = data.get("product_retailer_id", None)
        self.quantity: int = data.get("quantity", None)
        self.price: Union[float, int] = data.get("item_price", None)
        self.currency: str = data.get("currency", None)

    def __repr__(self):
        return f"Product(id={self.id}, quantity={self.quantity}, price={self.price}, currency={self.currency})"


class OrderMessage:
    def __init__(self, data: dict, user: User):
        self.id: str = data.get("id", None)
        self.user: User = user
        self.timestamp: str = data.get("timestamp", None)
        self.type: str = data.get("type", None)
        self.catalog_id = data.get("order", {}).get("catalog_id", None)
        self.order_text = data.get("order", {}).get("text", None)
        self.products = [
            Product(data) for data in data.get("order", {}).get("product_items", None)
        ]

    def __repr__(self):
        return f"OrderMessage(id={self.id}, timestamp={self.timestamp}, type={self.type}, catalog_id={self.catalog_id}, order_text={self.order_text}, products={self.products}, user={self.user})"
