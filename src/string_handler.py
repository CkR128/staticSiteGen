
import re
from typing import List, Tuple

from textnode import TextNode, TextType

def extract_all_markdown_images(text: str) -> List[Tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.+?)\)", text)

def extract_all_markdown_links(text: str) -> List[Tuple[str, str]]:
    return re.findall(r"(?<!!)\[(.*?)\]\((.+?)\)", text)

def split_node_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    stack = old_nodes
    result = []
    while len(stack) > 0:
        node = stack.pop(0)
        if len(stack) == 0 and node.text == "":
            break

        split = node.text.split(delimiter, 2)
        if len(split) == 1:
            result.append(node)
            continue

        if len(split) % 2 == 0:
            raise ValueError("Missing terminating delimiter.")

        result.append(TextNode(split[0], TextType.TEXT))
        result.append(TextNode(split[1], text_type))
        stack.insert(0, TextNode(split[2], TextType.TEXT))
    return result

def split_node_link(old_nodes: List[TextNode]) -> List[TextNode]:
    stack = old_nodes
    result = []
    while len(stack) > 0:
        node = stack.pop(0)
        if len(stack) == 0 and node.text == "":
            break

        split = node.text.split(delimiter, 2)
        if len(split) == 1:
            result.append(node)
            continue

        if len(split) % 2 == 0:
            raise ValueError("Missing terminating delimiter.")

        result.append(TextNode(split[0], TextType.TEXT))
        result.append(TextNode(split[1], text_type))
        stack.insert(0, TextNode(split[2], TextType.TEXT))
    return result
