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

    def test_forces_break(self):
        text = "SomeLongWord"
        result = break_text(text, 5)
        expected = ("Some-", "LongWord")
        self.assert_equal(result, expected)

    def test_uses_existing_soft_hyphen(self):
        text = "A line breaking ex·perience"
        result = break_text(text, 21)
        expected = ("A line breaking ex-" , "perience")
        self.assert_equal(result, expected)

    def test_uses_custom_hyphenation_character(self):
        text = "SomeLongWord"
        result = break_text(text, 5, hyphen="~")
        expected = ("Some~", "LongWord")
        self.assert_equal(result, expected)
