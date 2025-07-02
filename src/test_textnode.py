import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_link(self):
        node = TextNode("This is a text node", TextType.LINK, "boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "boot.dev")
        self.assertEqual(node, node2)

    def test_neq_link(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_neq_link_code(self):
        node = TextNode("This is a text node", TextType.LINK, "boot.dev")
        node2 = TextNode("This is a text node", TextType.CODE, "boot.dev")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
