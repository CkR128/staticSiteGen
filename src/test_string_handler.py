import unittest

from htmlnode import HTMLNode, LeafNode
from string_handler import extract_all_markdown_images, extract_all_markdown_links, split_node_delimiter, split_node_images, split_node_link, text_to_textnodes
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

    def test_extract_all_markdown_links(self):
        matches = extract_all_markdown_links("This is text with an [link](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_all_markdown_links("[link](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_all_markdown_links("[link](https://i.imgur.com/zjjcJKZ.png) this is other content [link2](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png"), ("link2", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_all_markdown_links("[link](https://i.imgur.com/zjjcJKZ.png) this is other content ![link2](https://i.imgur.com/zjjcJKZ.png) this is other content [link2](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png"), ("link2", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_all_markdown_images(self):
        matches = extract_all_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_all_markdown_images("![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_all_markdown_images("![image](https://i.imgur.com/zjjcJKZ.png) this is other content ![image2](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_all_markdown_images("![link](https://i.imgur.com/zjjcJKZ.png) this is other content [link2](https://i.imgur.com/zjjcJKZ.png) this is other content ![link2](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png"), ("link2", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_node_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_node_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_node_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnode(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        expected=[
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        
        for i in range(0, len(nodes) - 1):
            self.assertEqual(expected[i].text_type, nodes[i].text_type)
            self.assertEqual(expected[i].text, nodes[i].text)
