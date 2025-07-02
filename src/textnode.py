from enum import Enum
from typing import Optional

class TextType(Enum):
    TEXT="text"
    BOLD="bold"
    ITALIC="italic"
    CODE="code"
    LINK="link"
    IMAGE="image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: Optional[str] = None) -> None:
        super().__init__()
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        if self.text != other.text:
            return False
        if self.text_type != other.text_type:
            return False
        if self.url != other.url:
            return False
        return True
    def __repr__(self) -> str:
        if self.url != None:
            return f"textnode({self.text}, {self.text_type.value}, {self.url})"
        return f"textnode({self.text}, {self.text_type.value})"
