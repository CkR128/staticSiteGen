import re
from typing import List
from enum import Enum

class BlockType(Enum):
    PARAGRAPH="paragraph"
    HEADING="heading"
    CODE="code"
    QUOTE="quote"
    UNORDERED_LIST="unorderedList"
    ORDERED_LIST="orderedList"

def block_to_block_type(blockStr: str) -> BlockType:
    if re.match(r"#{1,6} .*", blockStr) != None:
        return BlockType.HEADING

    if re.match(r"^```.*?```$", blockStr, re.S) != None:
        return BlockType.CODE

    lines = blockStr.split("\n")
    quote = True
    unordered = True
    ordered = True
    for line in lines:
        if line == "":
            continue

        if quote and re.match(r"^>([ .*]|$)", line) == None:
            quote = False
        if unordered and re.match(r"^- .*", line) == None:
            unordered = False
        if ordered and re.match(r"[0-9]+\. .*", line) == None:
            ordered = False

        # If at least one is still true keep going.
        if quote or unordered or ordered:
            continue
        break

    if quote:
        return BlockType.QUOTE
    if unordered:
        return BlockType.UNORDERED_LIST
    if ordered:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_blocks(mdString: str) -> List[str]:
    blocks = mdString.split("\n\n")
    filtered = []
    for block in blocks:
        if block != "":
            filtered.append(block.strip())
    return filtered
