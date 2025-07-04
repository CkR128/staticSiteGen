from block_handler import BlockType, block_to_block_type, markdown_to_blocks

import unittest


class TestBlockHandler(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

        md = """
This is **bolded** paragraph   






This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line    

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        md = """
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line    
"""
        blocks = markdown_to_blocks(md)
        self.assertTrue(len(blocks) == 1)
        block = block_to_block_type(blocks[0])
        self.assertEqual(block, BlockType.PARAGRAPH)

        md = """
- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertTrue(len(blocks) == 1)
        block = block_to_block_type(blocks[0])
        self.assertEqual(block, BlockType.UNORDERED_LIST)

        md = """
1. This is a list
2. with items
"""
        blocks = markdown_to_blocks(md)
        self.assertTrue(len(blocks) == 1)
        block = block_to_block_type(blocks[0])
        self.assertEqual(block, BlockType.ORDERED_LIST)

        md = """
> This is a list
> with items
"""
        blocks = markdown_to_blocks(md)
        self.assertTrue(len(blocks) == 1)
        block = block_to_block_type(blocks[0])
        self.assertEqual(block, BlockType.QUOTE)

        md = """
> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
"""
        blocks = markdown_to_blocks(md)
        self.assertTrue(len(blocks) == 1)
        block = block_to_block_type(blocks[0])
        self.assertEqual(block, BlockType.QUOTE)

        md = """
###### This is a list
"""
        blocks = markdown_to_blocks(md)
        self.assertTrue(len(blocks) == 1)
        block = block_to_block_type(blocks[0])
        self.assertEqual(block, BlockType.HEADING)


        md = """
# This is a list
"""
        blocks = markdown_to_blocks(md)
        self.assertTrue(len(blocks) == 1)
        block = block_to_block_type(blocks[0])
        self.assertEqual(block, BlockType.HEADING)

        md = """
```
Codeblock...
```
"""
        blocks = markdown_to_blocks(md)
        self.assertTrue(len(blocks) == 1)
        block = block_to_block_type(blocks[0])
        self.assertEqual(block, BlockType.CODE)
