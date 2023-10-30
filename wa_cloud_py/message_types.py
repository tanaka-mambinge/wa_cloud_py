from enum import Enum
from typing import List, Union


class MessageType(str, Enum):
    """
    Enum representing the type of a message.
    """

    ORDER = "order"
    TEXT = "text"
    INTERACTIVE = "interactive"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    LOCATION = "location"
    REACTION = "reaction"


class MessageCategory(str, Enum):
    """
    Enum representing the category of a message.
    """

    SERVICE = "service"
    UTILITY = "utility"
    AUTHENTICATION = "authentication"
    MARKETING = "marketing"


class Status(str, Enum):
    """
    Enum representing the status of a message.
    """

    SENT = "sent"
    DELIVERED = "delivered"


class MessageStatus:
    """
    Class representing the status of a message.
    """

    def __init__(self, data: dict):
        self.id: str = data.get("id", None)
        self.status: str = data.get("status", None)
        self.timestamp: str = data.get("timestamp", None)
        self.recipient_phone: str = data.get("recipient_id", None)
        self.billable: bool = data.get("pricing", {}).get("billable", None)
        self.pricing_model: bool = data.get("pricing", {}).get("pricing_model", None)
        self.message_category: str = data.get("pricing", {}).get("category", None)

    def __repr__(self):
        return f"MessageStatus(id={self.id}, status={self.status}, timestamp={self.timestamp}, recipient_phone={self.recipient_phone}, billable={self.billable}, pricing_model={self.pricing_model}, message_category={self.message_category})"


class User:
    """
    Class representing a user.
    """

    def __init__(self, data: dict):
        self.name: str = data.get("profile", {}).get("name", None)
        self.phone_number: str = data.get("wa_id", None)

    def __repr__(self):
        return f"User(name={self.name}, phone_number={self.phone_number})"


class Product:
    """
    Class representing a product item in an order message.
    """

    def __init__(self, data: dict):
        self.id: str = data.get("product_retailer_id", None)
        self.quantity: int = data.get("quantity", None)
        self.price: Union[float, int] = data.get("item_price", None)
        self.currency: str = data.get("currency", None)

    def __repr__(self):
        return f"Product(id={self.id}, quantity={self.quantity}, price={self.price}, currency={self.currency})"


class UserMessage:
    """
    Class representing a message sent by a user.
    """

    def __init__(self, user: User):
        self.user: User = user


class InteractiveMessage(UserMessage):
    """
    Class representing an interactive message sent by a user.
    """

    def __init__(self, data: dict, user: User):
        super().__init__(user)
        self.id: str = data.get("id", None)
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


class TextMessage(UserMessage):
    """
    Class representing a text message sent by a user.
    """

    def __init__(self, data: dict, user: User):
        super().__init__(user)
        self.id: str = data.get("id", None)
        self.context_message_id: str = data.get("context", {}).get("id", None)
        self.timestamp: str = data.get("timestamp", None)
        self.type: str = data.get("type", None)
        self.body: str = data.get("text", {}).get("body", None)

    def __repr__(self):
        return f"TextMessage(id={self.id}, timestamp={self.timestamp}, type={self.type}, body={self.body}, user={self.user})"


class OrderMessage(UserMessage):
    """
    Class representing an order message sent by a user.
    """

    def __init__(self, data: dict, user: User):
        super().__init__(user)
        self.id: str = data.get("id", None)
        self.timestamp: str = data.get("timestamp", None)
        self.type: str = data.get("type", None)
        self.catalog_id: str = data.get("order", {}).get("catalog_id", None)
        self.order_text: str = data.get("order", {}).get("text", None)
        self.products: List[Product] = [
            Product(data) for data in data.get("order", {}).get("product_items", None)
        ]

    def __repr__(self):
        return f"OrderMessage(id={self.id}, timestamp={self.timestamp}, type={self.type}, catalog_id={self.catalog_id}, order_text={self.order_text}, products={self.products}, user={self.user})"
