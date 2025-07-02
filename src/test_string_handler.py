import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from string_handler import extract_markdown_images, extract_markdown_links, split_node_delimiter
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
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with an [link](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_markdown_links("[link](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_markdown_links("[link](https://i.imgur.com/zjjcJKZ.png) this is other content [link2](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png"), ("link2", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_markdown_links("[link](https://i.imgur.com/zjjcJKZ.png) this is other content ![link2](https://i.imgur.com/zjjcJKZ.png) this is other content [link2](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png"), ("link2", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_markdown_images("![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_markdown_images("![image](https://i.imgur.com/zjjcJKZ.png) this is other content ![image2](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_markdown_images("![link](https://i.imgur.com/zjjcJKZ.png) this is other content [link2](https://i.imgur.com/zjjcJKZ.png) this is other content ![link2](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png"), ("link2", "https://i.imgur.com/zjjcJKZ.png")], matches)
