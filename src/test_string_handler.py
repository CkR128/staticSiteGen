import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from string_handler import split_node_delimiter
from textnode import TextNode, TextType 

class TestStringHandler(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is text with a `code block` and another `code block with additional text` after the codeblock", TextType.TEXT)
        new_nodes = split_node_delimiter([node], "`", TextType.CODE)

        expectedTypes = [
            TextType.TEXT,
            TextType.CODE,
            TextType.TEXT,
            TextType.CODE,
            TextType.TEXT
        ]
        for i in range(0, len(new_nodes) - 1):
            self.assertEqual(expectedTypes[i], new_nodes[i].text_type)

    def test_complex_eq(self):
        node = TextNode("This is **text** with a `code block` and _another_ `code block with additional text` after _the codeblock_", TextType.TEXT)
        new_nodes = split_node_delimiter([node], "`", TextType.CODE)
        new_nodes = split_node_delimiter(new_nodes, "**", TextType.BOLD)
        new_nodes = split_node_delimiter(new_nodes, "_", TextType.ITALIC)

        expectedTypes = [
            TextType.TEXT,
            TextType.BOLD,
            TextType.TEXT,
            TextType.CODE,
            TextType.TEXT,
            TextType.ITALIC,
            TextType.TEXT,
            TextType.CODE,
            TextType.TEXT,
            TextType.ITALIC
        ]
        for i in range(0, len(new_nodes) - 1):
            self.assertEqual(expectedTypes[i], new_nodes[i].text_type)
