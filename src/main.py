import re
from typing import List
from block_handler import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import HTMLNode, LeafNode, ParentNode
from string_handler import text_to_textnodes
from textnode import TextNode, TextType
keepInLine=True

def text_to_htmlNode(block: str) -> List[LeafNode]:
    if keepInLine:
        block = block.replace("\n", " ")

    textNodes = text_to_textnodes(block)
    childNodes = []
    for node in textNodes:
        childNodes.append(node.text_node_to_html_node())

    return childNodes
def text_to_codeBlock(block: str) -> LeafNode:
    lines = block.splitlines()

    mapped = []
    for line in lines[1:-1]:
        mapped.append(line)
    mappedBlock = "\n".join(mapped)
    return LeafNode("code", mappedBlock)

def text_to_Heading(block: str) -> LeafNode:
    result = re.match(r"(#{1,6}) (.*)", block)
    if result == None:
        raise ValueError("Heading block not valid. This should never happen.")

    groups = result.groups()
    level = len(groups[0])
    content = groups[1]

    return LeafNode(f"h{level}", content)

def text_to_list(block: str) -> List[LeafNode]:
    lines = block.splitlines()

    mapped = []
    for line in lines:
        line = re.sub(r"^- ", "", line)
        line = re.sub(r"^[0-9]+\. ", "", line)

        children = text_to_htmlNode(line)
        mapped.append(LeafNode("li", line))
    return mapped

def markdown_to_html(mdString: str) -> HTMLNode:
    blocks = markdown_to_blocks(mdString)

    nodes = []
    for block in blocks:
        blockType = block_to_block_type(block)

        if blockType == BlockType.PARAGRAPH:
            childNodes = text_to_htmlNode(block)
            parentNode = ParentNode("p", childNodes)
            nodes.append(parentNode)
            continue

        if blockType == BlockType.CODE:
            codeNode = text_to_codeBlock(block)
            pre = ParentNode("pre", [codeNode])
            nodes.append(pre)
            continue

        if blockType == BlockType.HEADING:
            heading = text_to_Heading(block)
            nodes.append(heading)
            continue

        if blockType == BlockType.UNORDERED_LIST:
            lines = text_to_list(block)
            ul = ParentNode("ul", lines)
            nodes.append(ul)
            continue

        if blockType == BlockType.ORDERED_LIST:
            lines = text_to_list(block)
            ol = ParentNode("ol", lines)
            nodes.append(ol)
            continue

        if blockType == BlockType.QUOTE:
            lines = block.splitlines()
            newLines = []
            for line in lines:
                newLines.append(re.sub(r"^> ", "", line))
            block = "\n".join(newLines)

            childNodes = text_to_htmlNode(block)
            parentNode = ParentNode("blockquote", childNodes)
            nodes.append(parentNode)
            continue

    return ParentNode("div", nodes)

