import unittest

from htmlnode import HTMLNode, LeafNode
from markdown_handler import markdown_to_html
from page_hander import extract_title
from string_handler import extract_all_markdown_images, extract_all_markdown_links, split_node_delimiter, split_node_images, split_node_link, text_to_textnodes
from textnode import TextNode, TextType 

class TestPageHander(unittest.TestCase):
    def test_header(self):
        md = """

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

# Tolkien Fan Club

## Blog posts
"""
        title = extract_title(md)
        self.assertEqual(title, "Tolkien Fan Club")

        md = """
# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

## Blog posts
"""
        title = extract_title(md)
        self.assertEqual(title, "Tolkien Fan Club")
