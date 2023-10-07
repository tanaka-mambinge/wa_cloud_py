from typing import List


class CatalogSection:
    def __init__(self, title: str, retailer_product_ids: List[str]) -> None:
        self.title = title
        self.retailer_product_ids = retailer_product_ids

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "product_items": [
                {"product_retailer_id": _id} for _id in self.retailer_product_ids
            ],
        }


class ReplyButton:
    def __init__(self, id: str, title: str) -> None:
        self.id = id
        self.title = title

    def to_dict(self) -> dict:
        return {
            "type": "reply",
            "reply": {"id": self.id, "title": self.title},
        }


class SectionRow:
    def __init__(self, id: str, title: str, desc: str = "") -> None:
        self.id = id
        self.title = title
        self.desc = desc

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.desc,
        }


class ListSection:
    def __init__(self, title: str, rows: list[SectionRow]) -> None:
        self.title = title
        self.rows = rows

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "rows": [row.to_dict() for row in self.rows],
        }
