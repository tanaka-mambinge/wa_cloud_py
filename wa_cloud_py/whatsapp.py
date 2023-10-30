import json
from typing import List, Tuple, Union

import requests
from loguru import logger
from requests import Response

from wa_cloud_py.message_components import CatalogSection, ListSection, ReplyButton
from wa_cloud_py.message_types import (
    InteractiveMessage,
    MessageStatus,
    MessageType,
    OrderMessage,
    TextMessage,
    User,
)


class WhatsApp:
    """
    A class representing a WhatsApp instance.
    """

    def __init__(
        self,
        access_token: str,
        phone_number_id: str,
        version: str = "v18.0",
        verbose: bool = True,
    ) -> None:
        """
        Initializes a new instance of the WhatsApp class.

        Args:
            access_token (str): The access token for the WhatsApp instance.
            phone_number_id (str): The phone number ID for the WhatsApp instance.
            version (str, optional): The version of WhatsApp Cloud Api being used. Defaults to "18.0".
            verbose (bool, optional): Whether to enable logging. Defaults to True.
        """

        self.access_token = access_token
        self.phone_number_id = phone_number_id
        self.version = version
        self.messages_url = (
            f"https://graph.facebook.com/{self.version}/{self.phone_number_id}/messages"
        )
        self.commerce_url = f"https://graph.facebook.com/{self.version}/{self.phone_number_id}/whatsapp_commerce_settings"
        self.business_profile_url = f"https://graph.facebook.com/{self.version}/{self.phone_number_id}/whatsapp_business_profile"

        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        self.verbose = verbose

    def parse(
        self, request_data: dict
    ) -> Union[InteractiveMessage, TextMessage, OrderMessage, None]:
        """
        Parses a request from the WhatsApp Cloud API and returns a message object.

        Args:
            request_data (dict): The request data from the WhatsApp Cloud API.

        Returns:
            Union[InteractiveMessage, TextMessage, OrderMessage, None]: The parsed message object, or None if no messages were found.
        """

        msg_req: dict = json.loads(request_data)
        msg_value: dict = (
            msg_req.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {})
        )

        if len(msg_value.get("messages", [])) > 0:
            user = User(msg_value.get("contacts")[0])
            message_type = msg_value.get("messages")[0].get("type", None)

            if message_type == MessageType.TEXT:
                return TextMessage(msg_value.get("messages")[0], user=user)
            elif message_type == MessageType.INTERACTIVE:
                return InteractiveMessage(msg_value.get("messages")[0], user=user)
            elif message_type == MessageType.ORDER:
                return OrderMessage(msg_value.get("messages")[0], user=user)
            else:
                logger.error(f"Unsupported message type: {message_type}")
                return None
        elif len(msg_value.get("statuses", [])) > 0:
            status = msg_value.get("statuses")[0]
            return MessageStatus(status)

        else:
            logger.error("No messages found in request")
            return None

    def _parse_response(self, res: Response, phone_number: str) -> Tuple[bool, dict]:
        """
        Parses the response from the WhatsApp Cloud API and returns a tuple indicating whether the message was sent successfully
        and the response data.

        Args:
            res (Response): The response object returned by the WhatsApp Cloud API.
            phone_number (str): The phone number the message was sent to.

        Returns:
            Tuple[bool, dict]: A tuple containing a boolean indicating whether the message was sent successfully and a
            dictionary containing the response data.
        """

        if res.status_code == 200:
            if self.verbose:
                logger.success(f"Message sent to {phone_number}")
            return True, res.json()

        if self.verbose:
            logger.error(
                f"Failed to send message to {phone_number}.\nReason: {res.json()}"
            )
        return False, res.json()

    def send_text(
        self,
        to: str,
        body: str,
        preview_url: bool = True,
        context_message_id: str = None,
    ) -> Tuple[bool, dict]:
        """
        Sends a text message to the specified phone number using the WhatsApp Cloud API.

        Args:
            to (str): The phone number to send the message to.
            body (str): The body of the message to send.
            preview_url (bool, optional): Whether to include a preview URL in the message. Defaults to True.
            context_message_id (str, optional): The ID of the context message to reply to. Defaults to None.

        Returns:
            Tuple[bool, dict]: A tuple containing a boolean indicating whether the message was sent successfully and a
            dictionary containing the response data.
        """

        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": MessageType.TEXT,
            "text": {"preview_url": preview_url, "body": body},
        }

        if context_message_id is not None:
            data = {
                **data,
                "context": {"message_id": context_message_id},
            }

        res = requests.post(self.messages_url, headers=self.headers, json=data)
        return self._parse_response(res, phone_number=to)

    def send_reaction(self, to: str, message_id: str, emoji: str) -> Tuple[bool, dict]:
        """
        Sends a reaction to a message in a WhatsApp chat.

        Args:
            to (str): The phone number of the recipient of the message.
            message_id (str): The ID of the message to react to.
            emoji (str): The emoji to use as the reaction.

        Returns:
            Tuple[bool, dict]: A tuple containing a boolean indicating whether the reaction was sent successfully and a
            dictionary containing the response data.
        """

        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": MessageType.REACTION,
            "reaction": {"message_id": message_id, "emoji": emoji},
        }

        res = requests.post(self.messages_url, headers=self.headers, json=data)
        return self._parse_response(res, phone_number=to)

    def send_location(
        self, to: str, name: str, address: str, latitude: float, longitude: float
    ) -> Tuple[bool, dict]:
        """
        Sends a location message to the specified phone number using the WhatsApp Cloud API.

        Args:
            to (str): The phone number to send the message to.
            name (str): The name of the location.
            address (str): The address of the location.
            latitude (float): The latitude of the location.
            longitude (float): The longitude of the location.

        Returns:
            Tuple[bool, dict]: A tuple containing a boolean indicating whether the message was sent successfully and a
            dictionary containing the response data.
        """

        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": MessageType.LOCATION,
            "location": {
                "longitude": longitude,
                "latitude": latitude,
                "name": name,
                "address": address,
            },
        }

        res = requests.post(self.messages_url, headers=self.headers, json=data)
        return self._parse_response(res, phone_number=to)

    def send_image(self, to: str, url: str, caption: str = None) -> Tuple[bool, dict]:
        """
        Sends an image message to the specified phone number using the WhatsApp Cloud API.

        Args:
            to (str): The phone number to send the message to.
            url (str): The URL of the image to send.
            caption (str, optional): The caption to include with the image. Defaults to None.

        Returns:
            Tuple[bool, dict]: A tuple containing a boolean indicating whether the message was sent successfully and a
            dictionary containing the response data.
        """

        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": MessageType.IMAGE,
            "image": {"link": url},
        }

        if caption is not None:
            data["image"]["caption"] = caption

        res = requests.post(self.messages_url, headers=self.headers, json=data)
        return self._parse_response(res, phone_number=to)

    def send_video(self, to: str, url: str, caption: str = None) -> Tuple[bool, dict]:
        """
        Sends a video message to the specified phone number using the WhatsApp Cloud API.

        Args:
            to (str): The phone number to send the message to.
            url (str): The URL of the video to send.
            caption (str, optional): The caption to include with the video. Defaults to None.

        Returns:
            Tuple[bool, dict]: A tuple containing a boolean indicating whether the message was sent successfully and a
            dictionary containing the response data.
        """

        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": MessageType.VIDEO,
            "video": {"link": url},
        }

        if caption is not None:
            data["video"]["caption"] = caption

        res = requests.post(self.messages_url, headers=self.headers, json=data)
        return self._parse_response(res, phone_number=to)

    def send_audio(self, to: str, url: str) -> Tuple[bool, dict]:
        """
        Sends a video message to the specified phone number using the WhatsApp Cloud API.

        Args:
            to (str): The phone number to send the message to.
            url (str): The URL of the audio to send.

        Returns:
            Tuple[bool, dict]: A tuple containing a boolean indicating whether the message was sent successfully and a
            dictionary containing the response data.
        """

        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": MessageType.AUDIO,
            "audio": {"link": url},
        }

        res = requests.post(self.messages_url, headers=self.headers, json=data)
        return self._parse_response(res, phone_number=to)

    def send_document(
        self, to: str, url: str, caption: str = None, filename: str = None
    ) -> Tuple[bool, dict]:
        """
        Sends a document message to the specified phone number using the WhatsApp Cloud API.

        Args:
            to (str): The phone number to send the message to.
            url (str): The URL of the document to send.
            caption (str, optional): The caption to include with the document. Defaults to None.
            filename (str, optional): The filename of the document. Defaults to None.
        """

        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": MessageType.DOCUMENT,
            "document": {"link": url},
        }

        if caption is not None:
            data["document"]["caption"] = caption

        if filename is not None:
            data["document"]["filename"] = filename

        res = requests.post(self.messages_url, headers=self.headers, json=data)
        return self._parse_response(res, phone_number=to)

    def send_interactive_buttons(
        self, to: str, body: str, buttons: List[ReplyButton]
    ) -> Tuple[bool, dict]:
        """
        Sends an interactive button message to the specified phone number using the WhatsApp Cloud API.

        Args:
            to (str): The phone number to send the message to.
            body (str): The body text of the message.
            buttons (List[ReplyButton]): A list of up to 3 buttons to include with the message.

        Returns:
            Tuple[bool, dict]: A tuple containing a boolean indicating whether the message was sent successfully and a
            dictionary containing the response data.
        """

        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": MessageType.INTERACTIVE,
            "interactive": {
                "type": "button",
                "body": {"text": body},
                "action": {"buttons": [button.to_dict() for button in buttons]},
            },
        }

        res = requests.post(self.messages_url, headers=self.headers, json=data)
        return self._parse_response(res, phone_number=to)

    def send_interactive_list(
        self,
        to: str,
        body: str,
        button: str,
        sections: List[ListSection],
        header: str = None,
        footer: str = None,
    ) -> Tuple[bool, dict]:
        """
        Sends an interactive list message to the specified phone number using the WhatsApp Cloud API.

        Args:
            to (str): The phone number to send the message to.
            body (str): The body text of the message.
            button (str): The text to display on the button.
            sections (List[ListSection]): A list of sections to include in the interactive list message.
            header (str, optional): The header text to include above the list. Defaults to None.
            footer (str, optional): The footer text to include below the list. Defaults to None.

        Returns:
            Tuple[bool, dict]: A tuple containing a boolean indicating whether the message was sent successfully and a
            dictionary containing the response data.
        """

        header = {"type": "text", "text": header} if header else None
        footer = {"text": footer}
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": MessageType.INTERACTIVE,
            "interactive": {
                "type": "list",
                "header": {"type": "text", "text": ""},
                "body": {"text": body},
                "footer": {"text": "FOOTER_TEXT"},
                "action": {
                    "button": button,
                    "sections": [section.to_dict() for section in sections],
                },
            },
        }

        if header:
            data["interactive"]["header"] = header

        if footer:
            data["interactive"]["footer"] = footer

        res = requests.post(self.messages_url, headers=self.headers, json=data)
        return self._parse_response(res, phone_number=to)

    def send_catalog(self, to: str, body: str, footer: str = None):
        """
        Sends a product catalog to the specified phone number using the WhatsApp Cloud API.

        Args:
            to (str): The phone number to send the message to.
            body (str): The body text of the message.
            footer (str, optional): The footer text to include below the message. Defaults to None.

        Returns:
            Tuple[bool, dict]: A tuple containing a boolean indicating whether the message was sent successfully and a
            dictionary containing the response data.
        """

        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": MessageType.INTERACTIVE,
            "interactive": {
                "type": "catalog_message",
                "body": {
                    "text": body,
                },
                "action": {
                    "name": "catalog_message",
                },
            },
        }

        if footer:
            data["interactive"]["footer"] = {"text": footer}

        res = requests.post(self.messages_url, headers=self.headers, json=data)
        return self._parse_response(res, phone_number=to)

    def send_catalog_product(
        self,
        to: str,
        product_retailer_id: str,
        catalog_id: str,
        body: str,
        footer: str = None,
    ):
        """
        Sends a product from your catalog to the specified phone number using the WhatsApp Cloud API.

        Args:
            to (str): The phone number to send the message to.
            product_retailer_id (str): The ID of your product.
            catalog_id (str): The ID of the catalog.
            body (str): The body text of the message.
            footer (str, optional): The footer text to include below the message. Defaults to None.

        Returns:
            Tuple[bool, dict]: A tuple containing a boolean indicating whether the message was sent successfully and a
            dictionary containing the response data.
        """

        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": MessageType.INTERACTIVE,
            "interactive": {
                "type": "product",
                "body": {"text": body},
                "action": {
                    "catalog_id": catalog_id,
                    "product_retailer_id": product_retailer_id,
                },
            },
        }

        if footer:
            data["interactive"]["footer"] = {"text": footer}

        res = requests.post(self.messages_url, headers=self.headers, json=data)
        return self._parse_response(res, phone_number=to)

    def send_catalog_product_list(
        self,
        to: str,
        catalog_id: str,
        header: str,
        body: str,
        product_sections: List[CatalogSection],
        footer: str = None,
    ):
        """
        Sends a lsit of products from your catalog to the specified phone number using the WhatsApp Cloud API.

        Args:
            to (str): The phone number to send the message to.
            catalog_id (str): The ID of the catalog.
            header (str): The header text of the message.
            body (str): The body text of the message.
            product_sections (List[CatalogSection]): A list of CatalogSection objects representing the product sections to include in the message.
            footer (str, optional): The footer text to include below the message. Defaults to None.

        Returns:
            Tuple[bool, dict]: A tuple containing a boolean indicating whether the message was sent successfully and a
            dictionary containing the response data.
        """

        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": MessageType.INTERACTIVE,
            "interactive": {
                "type": "product_list",
                "header": {"type": "text", "text": header},
                "body": {"text": body},
                "action": {
                    "catalog_id": catalog_id,
                    "sections": [section.to_dict() for section in product_sections],
                },
            },
        }

        if footer:
            data["interactive"]["footer"] = {"text": footer}

        res = requests.post(self.messages_url, headers=self.headers, json=data)
        return self._parse_response(res, phone_number=to)

    def mark_as_read(self, message_id: str) -> Tuple[bool, dict]:
        """
        Marks a message with the specified ID as read using the WhatsApp Cloud API.

        Args:
            message_id (str): The ID of the message to mark as read.

        Returns:
            Tuple[bool, dict]: A tuple containing a boolean indicating whether the message was marked as read successfully
            and a dictionary containing the response data.
        """

        data = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id,
        }

        res = requests.post(self.messages_url, headers=self.headers, json=data)

        if res.status_code == 200:
            if self.verbose:
                logger.success(f"Message with ID {message_id} marked as read")
            return True, res.json()

        if self.verbose:
            logger.error(
                f"Failed to mark message with ID {message_id} as read.\nReason: {res.json()}"
            )
        return False, res.json()

    def update_business_profile(
        self,
        about: str = "",
        address: str = "",
        description: str = "",
        email: str = "",
        vertical: str = "",
        websites: List[str] = [],
    ) -> Tuple[bool, dict]:
        """
        Updates the business profile using the WhatsApp Business API.

        Args:
            about (str, optional): A short description of the business. Defaults to "".
            address (str, optional): The address of the business. Defaults to "".
            description (str, optional): A longer description of the business. Defaults to "".
            email (str, optional): The email address of the business. Defaults to "".
            vertical (str, optional): The vertical of the business. Defaults to "".
            websites (List[str], optional): A list of website URLs associated with the business. Defaults to [].

        Returns:
            Tuple[bool, dict]: A tuple containing a boolean indicating whether the business profile was updated successfully
            and a dictionary containing the response data.
        """

        data = {
            "messaging_product": "whatsapp",
            "vertical": vertical,
        }

        if about:
            data["about"] = about
        if address:
            data["address"] = address
        if description:
            data["description"] = description
        if email:
            data["email"] = email
        if websites:
            data["websites"] = websites

        res = requests.post(self.business_profile_url, headers=self.headers, json=data)

        if res.status_code == 200:
            if self.verbose:
                logger.success(f"Business profile updated successfully")
            return True, res.json()

        if self.verbose:
            logger.error(f"Failed to update business profile.\nReason: {res.json()}")
        return False, res.json()

    def update_cart_status(self, is_cart_visible: bool) -> Tuple[bool, dict]:
        """
        Updates the cart status using the WhatsApp Commerce API.

        Args:
            is_cart_visible (bool): A boolean indicating whether the cart should be visible.

        Returns:
            Tuple[bool, dict]: A tuple containing a boolean indicating whether the cart status was updated successfully and a
            dictionary containing the response data.
        """

        res = requests.post(
            self.commerce_url,
            headers=self.headers,
            params={"is_cart_enabled": is_cart_visible},
        )

        if res.status_code == 200:
            if self.verbose:
                logger.success(f"Cart status updated successfully")
            return True, res.json()

        if self.verbose:
            logger.error(f"Failed to update cart status.\nReason: {res.json()}")
        return False, res.json()

    def update_catalog_status(self, is_catalog_visible: bool) -> Tuple[bool, dict]:
        """
        Updates the catalog status using the WhatsApp Commerce API.

        Args:
            is_catalog_visible (bool): A boolean indicating whether the catalog should be visible.

        Returns:
            Tuple[bool, dict]: A tuple containing a boolean indicating whether the catalog status was updated successfully and
            a dictionary containing the response data.
        """

        res = requests.post(
            self.commerce_url,
            headers=self.headers,
            params={"is_catalog_visible": is_catalog_visible},
        )

        if res.status_code == 200:
            if self.verbose:
                logger.success(f"Catalog status updated successfully")
            return True, res.json()

        if self.verbose:
            logger.error(f"Failed to update catalog status.\nReason: {res.json()}")
        return False, res.json()

    def commerce_settings(self):
        """
        Retrieves the commerce settings using the WhatsApp Commerce API.

        Returns:
            Tuple[bool, dict]: A tuple containing a boolean indicating whether the commerce settings were retrieved
            successfully and a dictionary containing the response data.
        """

        res = requests.get(
            self.commerce_url,
            headers=self.headers,
        )

        if res.status_code == 200:
            if self.verbose:
                logger.success(f"Commerce settings retrieved successfully")
            return True, res.json()

        if self.verbose:
            logger.error(f"Failed to retrieve commerce settings.\nReason: {res.json()}")
        return False, res.json()
