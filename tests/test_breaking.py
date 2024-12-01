from uneedtest import TestCase

from tamal.wrap import break_text

class TestBreakText(TestCase):

    def test_does_not_break_when_not_necessary(self):
        text = "A line breaking experience"
        result = break_text(text, 100)
        expected = ("A line breaking experience", "")
        self.assert_equal(result, expected)

    def test_uses_whitespace(self):
        text = "A line breaking experience"
        result = break_text(text, 11)
        expected = ("A line", "breaking experience")
        self.assert_equal(result, expected)

    def test_uses_existing_hyphen(self):
        text = "A line-breaking experience"
        result = break_text(text, 11)
        expected = ("A line-", "breaking experience")
        self.assert_equal(result, expected)
