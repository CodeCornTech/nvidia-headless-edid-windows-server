"""Offline checks for the self-hosted stars badge renderer."""
import unittest
import xml.etree.ElementTree as ET

from scripts.refresh_stars import render_badge


class BadgeTests(unittest.TestCase):
    def test_zero(self):
        svg = render_badge(0)
        root = ET.fromstring(svg)
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertEqual(root.attrib["aria-label"], "GitHub Stars: 0")

    def test_large_count(self):
        svg = render_badge(123456)
        self.assertIn(">123456</text>", svg)
        ET.fromstring(svg)

    def test_reject_invalid_count(self):
        for count in (-1, 1.5, "1", None, True):
            with self.subTest(count=count), self.assertRaises(ValueError):
                render_badge(count)


if __name__ == "__main__":
    unittest.main()
