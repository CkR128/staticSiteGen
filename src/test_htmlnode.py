import unittest

from htmlnode import HTMLNode 


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        tag: str = "a"
        value: str = "value text"
        children = None
        props = {"href": "https://www.google.com"}
        node = HTMLNode(tag, value, children, props)
        self.assertEqual(f"{node}".strip(), f"tag: '{tag}'\nvalue: '{value}'\nprops: ' href=https://www.google.com'\nchildren:\n    ".strip())

    def test_eq_2(self):
        tag: str = "a"
        value: str = "value text"
        children = None
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = HTMLNode(tag, value, children, props)
        self.assertEqual(f"{node}".strip(), f"tag: '{tag}'\nvalue: '{value}'\nprops: ' href=https://www.google.com target=_blank'\nchildren:\n    ".strip())

    def test_eq_Children(self):
        tag: str = "a"
        value: str = "value text"
        children = [
            HTMLNode("p", "This is a paragraph", None, None)
        ]
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = HTMLNode(tag, value, children, props)
        self.assertEqual(f"{node}".strip(), (
f"tag: '{tag}'\n"
f"value: '{value}'\n"
f"props: ' href=https://www.google.com target=_blank'\n"
f"children:\n"
f"    tag: 'p'\nvalue: 'This is a paragraph'\nprops: ''\nchildren:    \n".strip()))

    def test_eq_PropsToHTML(self):
        tag: str = "a"
        value: str = "value text"
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = HTMLNode(tag, value, None, props)
        self.assertEqual(node.props_to_html(), " href=https://www.google.com target=_blank")

    def test_eq_PropsToHTML_2(self):
        tag: str = "a"
        value: str = "value text"
        props = {"href": "https://www.google.com"}
        node = HTMLNode(tag, value, None, props)
        self.assertEqual(node.props_to_html(), " href=https://www.google.com")

if __name__ == "__main__":
    unittest.main()
