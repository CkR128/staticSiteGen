import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode 


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

class TestLeafNode(unittest.TestCase):
    def test_leaf_eq(self):
        tag="p"
        value="Hello world"
        props={"href": "https://www.google.com"}
        leaf = LeafNode(tag, value, props)
        propsStr = " href=https://www.google.com"
        result=f"<{tag}{propsStr}>{value}</{tag}>"
        self.assertEqual(leaf.to_html(), result)

    def test_leaf_eq_2(self):
        tag="p"
        value="Hello world"
        props=None
        leaf = LeafNode(tag, value, props)
        propsStr = ""
        result=f"<{tag}{propsStr}>{value}</{tag}>"
        self.assertEqual(leaf.to_html(), result)

class TestParentNode(unittest.TestCase):
    def test_parent_eq(self):
        node = ParentNode("p", [
            LeafNode("b", "Bold"),
            LeafNode(None, "Normal"),
            LeafNode("i", "italic"),
            LeafNode(None, "Normal")
        ])
        self.assertEqual(node.to_html(), "<p><b>Bold</b>Normal<i>italic</i>Normal</p>")

    def test_leaf_eq_2(self):
        node = ParentNode("p", [
            LeafNode("b", "Bold"),
        ])
        self.assertEqual(node.to_html(), "<p><b>Bold</b></p>")

if __name__ == "__main__":
    unittest.main()
