from typing import List


class CatalogSection:
    """
    A class representing a section of a catalog.
    """

    def __init__(self, title: str, retailer_product_ids: List[str]) -> None:
        """

        Args:
            title (str): The title of the section.
            retailer_product_ids (List[str]): A list of retailer product IDs.
        """
        self.title = title
        self.retailer_product_ids = retailer_product_ids

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the CatalogSection object.

        Returns:
            dict: A dictionary representation of the CatalogSection object.
        """
        return {
            "title": self.title,
            "product_items": [
                {"product_retailer_id": _id} for _id in self.retailer_product_ids
            ],
        }


class ReplyButton:
    """
    A class representing a reply button.
    """

    def __init__(self, id: str, title: str) -> None:
        """

        Args:
            id (str): The ID of the reply button.
            title (str): The title of the reply button.
        """
        self.id = id
        self.title = title

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the ReplyButton object.

        Returns:
            dict: A dictionary representation of the ReplyButton object.
        """
        return {
            "type": "reply",
            "reply": {"id": self.id, "title": self.title},
        }


class SectionRow:
    """
    A class representing a row in a section.
    """

    def __init__(self, id: str, title: str, description: str = "") -> None:
        """

        Args:
            id (str): The ID of the row.
            title (str): The title of the row.
            description (str, optional): The description of the row. Defaults to "".
        """
        self.id = id
        self.title = title
        self.description = description

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the SectionRow object.

        Returns:
            dict: A dictionary representation of the SectionRow object.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
        }


class ListSection:
    """
    A class representing a list section.
    """

    def __init__(self, title: str, rows: list[SectionRow]) -> None:
        """
        Args:
            title (str): The title of the list section.
            rows (list[SectionRow]): A list of SectionRow objects.
        """
        self.title = title
        self.rows = rows

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the ListSection object.

        Returns:
            dict: A dictionary representation of the ListSection object.
        """
        return {
            "title": self.title,
            "rows": [row.to_dict() for row in self.rows],
        }
