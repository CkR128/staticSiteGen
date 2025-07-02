from typing import List, Optional

class HTMLNode:
    def __init__(self, tag: str, value: str, children: Optional[List['HTMLNode']], props: Optional[dict[str, str]]) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        result = ""
        if self.props:
            for key, value in self.props.items():
                result += f" {key}={value}"
        return result

    def __repr__(self) -> str:
        children="    "
        if self.children:
            for child in self.children:
                children += child.__repr__()
                children += "\n    "
        return f"tag: '{self.tag}'\nvalue: '{self.value}'\nprops: '{self.props_to_html()}'\nchildren:\n{children}"
