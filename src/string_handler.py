
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

        links = extract_all_markdown_links(node.text)
        if len(links) == 0:
            result.append(node)
            continue
        nextLink = links[0]

        split = node.text.split(f"[{nextLink[0]}]({nextLink[1]})")
        if len(split) == 1:
            raise ValueError("Somehow splitting on link failed. This should not be possible.")

        result.append(TextNode(split[0], TextType.TEXT))
        result.append(TextNode(nextLink[0], TextType.LINK, nextLink[1]))
        stack.insert(0, TextNode(split[1], TextType.TEXT))

    return result

def split_node_images(old_nodes: List[TextNode]) -> List[TextNode]:
    stack = old_nodes
    result = []
    while len(stack) > 0:
        node = stack.pop(0)

        if len(stack) == 0 and node.text == "":
            break

        links = extract_all_markdown_images(node.text)
        if len(links) == 0:
            result.append(node)
            continue
        nextLink = links[0]

        split = node.text.split(f"![{nextLink[0]}]({nextLink[1]})")
        if len(split) == 1:
            raise ValueError("Somehow splitting on link failed. This should not be possible.")

        result.append(TextNode(split[0], TextType.TEXT))
        result.append(TextNode(nextLink[0], TextType.IMAGE, nextLink[1]))
        stack.insert(0, TextNode(split[1], TextType.TEXT))

    return result

def text_to_textnodes(text: str) -> List[TextNode]:
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_node_delimiter([node], "`", TextType.CODE)
    new_nodes = split_node_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_node_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_node_images(new_nodes)
    new_nodes = split_node_link(new_nodes)
    return new_nodes
