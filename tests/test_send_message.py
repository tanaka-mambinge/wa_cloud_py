import os
import unittest
from re import S

from dotenv import load_dotenv

from chatterbox import WhatsApp
from chatterbox.message_components import (
    CatalogSection,
    ListSection,
    ReplyButton,
    SectionRow,
)
from chatterbox.verticals import BusinessVertical

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

    def test_send_audio(self):
        message_sent, response = whatsapp.send_audio(
            to=recipient_phone,
            url="https://cdn.pixabay.com/download/audio/2022/04/25/audio_2a12b61cc0.mp3?filename=virtualitymusik-instrument-yopee-saturdae-110081.mp3&g-recaptcha-response=03AFcWeA5L_YPC483UDFXlUDtv7VnIpwAV1NJ17pxVMqP7WC2-CVyFA1guJT-6Pg1uc8iGJZ5Z_isyWDBfDl2vh4YcrTcpP9NnP9TkGjpwupvK5NojbhLt8gyz1q7JpqIAsjWwXRa9mKk00z9ml9Ee8LfGHymiPuIeWJEPVwUZEfxPHKHCBC0pa6XHvQzpfKwBE-cEQXqXqRWOkcLmVEavQNWyYhaUnnAVgKIMyvHN61aR-fZhXIAEOOo_j1CHhAlSsLI0ozIYE8CmhlHbx0WcSH1lZOj0WFa0bGXsIJ8f5soDbQJv66wMRSOEssUkwyU6EAU9jlMwaM0Ui44nyRyCmAyBcz74K6paWn3QrvGyGgwtJjl8-Z_gizOycTG2N5UxU0hyP9EeJOrSOtcPwhZeWdskEFub41I8SSL54XjBw3lIh0-ZswAsrSdcUYn4yqvkOYV3gtFRtsXLAnomoLJ0o3WlLBeG1SF1v31gN8jxgos1iTwtQ6pXNg93ZnjTym4wh3BecTzTuTH5oHRVWNpfT3DLLmdV8P4oryjPUIxp_C5qLwvpalisJ9ydHcOSWZBzG8zpOxNUYdxLLnmHxJFe3c-XQ7q-e9jfjA&remote_template=1",
        )
        self.assertTrue(message_sent)

    def test_send_document(self):
        message_sent, response = whatsapp.send_document(
            to=recipient_phone,
            url="https://business.facebook.com/products/feed_template/?feed_type=products&include_only_subvertical_fields=false&is_excel_template=false&item_capabilities[0]=mini_shops&file_type=CSV&is_supplementary_feed=false&catalog_id=1282347042264709",
            filename="products.csv",
            caption="WhatsApp online products template",
        )
        self.assertTrue(message_sent)

    def test_send_video(self):
        message_sent, response = whatsapp.send_video(
            to=recipient_phone,
            url="https://www.pexels.com/download/video/4812205/",
            caption="Beautiful flowers",
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

    def test_update_business_profile(self):
        message_sent, response = whatsapp.update_business_profile(
            about="We sell the best products",
            email="support@business.com",
            address="1600 Amphitheatre Parkway",
            description="We sell the best products",
            websites=["https://business.com"],
            vertical=BusinessVertical.RETAIL,
        )
        self.assertTrue(message_sent)
