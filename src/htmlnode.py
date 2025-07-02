from typing import List, Optional, Any


class HTMLNode:
    def __init__(self, tag: Optional[str] = None, value: Optional[str] = None, children: Optional[List[Any]] = None, props: Optional[dict[str, str]] = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        result = ""
        if self.props:
            for key, value in self.props.items():
                result += f" {key}={value}"
        return result

    def __repr__(self) -> str:
        children = "    "
        if self.children:
            for child in self.children:
                children += child.__repr__()
                children += "\n    "
        return f"tag: '{self.tag}'\nvalue: '{self.value}'\nprops: '{self.props_to_html()}'\nchildren:\n{children}"


class LeafNode(HTMLNode):
    def __init__(self, tag: Optional[str], value: str, props: Optional[dict[str, str]] = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError("No value in leaf node.")

        if self.tag == None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: List[LeafNode], props: Optional[dict[str, str]]=None) -> None:
        super().__init__(tag, None, children, props)
        self.children = children

    def to_html(self) -> str:
        if self.tag == None:
            raise ValueError("Tag not defined")

        if self.children == None:
            raise ValueError("No children definied on Parent")

        content=""
        for child in self.children:
            content += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{content}</{self.tag}>"
