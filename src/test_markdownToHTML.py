import unittest

from htmlnode import HTMLNode, LeafNode
from main import markdown_to_html
from string_handler import extract_all_markdown_images, extract_all_markdown_links, split_node_delimiter, split_node_images, split_node_link, text_to_textnodes
from textnode import TextNode, TextType 

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_ordered(self):
        md = """
1. one
2. two
3. three
"""
        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>one</li><li>two</li><li>three</li></ol></div>",
        )

    def test_unordered(self):
        md = """
- one
- two
- three
"""
        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>one</li><li>two</li><li>three</li></ul></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_heading(self):
        md = """
# Heading 1
"""
        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><h1>Heading 1</h1></div>",
        )

        md = """
## Heading 2
"""
        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><h2>Heading 2</h2></div>",
        )

        md = """
### Heading 3
"""
        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><h3>Heading 3</h3></div>",
        )

        md = """
#### Heading 4
"""
        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><h4>Heading 4</h4></div>",
        )

        md = """
##### Heading 5
"""
        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><h5>Heading 5</h5></div>",
        )

        md = """
###### Heading 6
"""
        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><h6>Heading 6</h6></div>",
        )

