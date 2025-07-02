
from textnode import TextNode, TextType


t = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
print(t)
