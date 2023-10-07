import os
import unittest
from re import S

from dotenv import load_dotenv

from chatterbox import WhatsApp
from chatterbox.messages.components import (
    CatalogSection,
    ListSection,
    ReplyButton,
    SectionRow,
)

load_dotenv()

whatsapp = WhatsApp(
    access_token=os.getenv("WHATSAPP_ACCESS_TOKEN"),
    phone_number_id=os.getenv("WHATSAPP_PHONE_NUMBER_ID"),
)

recipient_phone = os.getenv("RECIPIENT_PHONE")
catalog_id = "1282347042264709"
product_id = "4f809a0c-7ee7-4120-a1c4-5110ef302a9f"
product_ids = [
    "91a75fd5-7f0b-4ae4-b90f-f255d8d08e27",
    "0c61d2da-4d34-4841-8660-80ca7669c188",
    "d759f233-111b-4d97-9f84-ab1e98bc2966",
]


class SendMessage(unittest.TestCase):
    def test_send_text(self):
        message_sent, response = whatsapp.send_text(
            to=recipient_phone, body="Hello World"
        )
        self.assertTrue(message_sent)

    def test_send_text_with_context(self):
        # send message
        message_sent, response = whatsapp.send_text(
            to=recipient_phone, body="I'm going to be replied to"
        )
        self.assertTrue(message_sent)

        # reply to message
        message_id = response["messages"][0]["id"]
        message_sent, response = whatsapp.send_text(
            to=recipient_phone,
            body="You've been replied",
            context_message_id=message_id,
        )
        self.assertTrue(message_sent)

    def test_send_reaction(self):
        # send message
        message_sent, response = whatsapp.send_text(
            to=recipient_phone, body="I'm going to receive a reaction"
        )
        self.assertTrue(message_sent)

        # react to message
        message_id = response["messages"][0]["id"]
        message_sent, response = whatsapp.send_reaction(
            to=recipient_phone, message_id=message_id, emoji="😲"
        )
        self.assertTrue(message_sent)

    def test_send_location(self):
        message_sent, response = whatsapp.send_location(
            to=recipient_phone,
            name="Google head offices",
            address="1600 Amphitheatre Parkway, Mountain View, CA",
            latitude="37.422",
            longitude="-122.084",
        )
        self.assertTrue(message_sent)

    def test_send_interactive_buttons(self):
        message_sent, response = whatsapp.send_interactive_buttons(
            to=recipient_phone,
            body="Confirm your purchase",
            buttons=[
                ReplyButton(id="confirm", title="Confirm"),
                ReplyButton(id="cancel", title="Cancel"),
            ],
        )
        self.assertTrue(message_sent)

    def test_send_interactive_list(self):
        message_sent, response = whatsapp.send_interactive_list(
            to=recipient_phone,
            header="Payment options",
            body="Select a payment option 🧾",
            button="Options",
            sections=[
                ListSection(
                    title="Mobile money 📱",
                    rows=[
                        SectionRow(
                            id="pay_with_ecocash",
                            title="EcoCash",
                            description="Pay with EcoCash",
                        ),
                        SectionRow(
                            id="pay_with_onemoney",
                            title="OneMoney",
                            description="Pay with OneMoney",
                        ),
                    ],
                ),
                ListSection(
                    title="Bank transfer 💳",
                    rows=[
                        SectionRow(id="pay_with_visa", title="Visa"),
                        SectionRow(id="pay_with_mastercard", title="MasterCard"),
                    ],
                ),
            ],
        )
        self.assertTrue(message_sent)

    def test_send_image(self):
        message_sent, response = whatsapp.send_image(
            to=recipient_phone,
            url="https://images.unsplash.com/photo-1622618760546-8e443f8a909b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8c2hpYmElMjBpbnV8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60",
            caption="So much wow",
        )
        self.assertTrue(message_sent)

    def test_send_catalog(self):
        message_sent, response = whatsapp.send_catalog(
            to=recipient_phone, body="Have a look at our products 🛍"
        )
        self.assertTrue(message_sent)

    def test_send_product_from_catalog(self):
        message_sent, response = whatsapp.send_catalog_product(
            to=recipient_phone,
            catalog_id=catalog_id,
            product_retailer_id=product_id,
            body="Samsung Galaxy M04",
        )
        self.assertTrue(message_sent)

    def test_send_product_list_from_catalog(self):
        message_sent, response = whatsapp.send_catalog_product_list(
            to=recipient_phone,
            catalog_id="1282347042264709",
            header="Products",
            body="Select a product and add it to the cart 🛒",
            product_sections=[
                CatalogSection(title="Phones", retailer_product_ids=[product_ids[0]]),
                CatalogSection(
                    title="Frequently bought with",
                    retailer_product_ids=product_ids[1:],
                ),
            ],
        )
        self.assertTrue(message_sent)

    def test_update_catalog_status(self):
        message_sent, response = whatsapp.update_catalog_status(is_catalog_visible=True)
        self.assertTrue(message_sent)

    def test_update_cart_status(self):
        message_sent, response = whatsapp.update_cart_status(is_cart_visible=True)
        self.assertTrue(message_sent)

    def test_get_commerce_settings(self):
        message_sent, response = whatsapp.commerce_settings()
        self.assertTrue(message_sent)
