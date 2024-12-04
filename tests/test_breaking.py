from uneedtest import TestCase

from tamal import break_lines, chunk


class TestChunk(TestCase):

    def test_does_not_break_when_not_necessary(self):
        text = "A line breaking experience"
        result = chunk(text, 100)
        expected = ("A line breaking experience", "")
        self.assert_equal(result, expected)

    def test_breaks_and_removes_whitespaces(self):
        text = "A line breaking experience"
        result = chunk(text, 11)
        expected = ("A line", "breaking experience")
        self.assert_equal(result, expected)

    def test_breaks_and_removes_tab(self):
        text = "A line\tbreaking experience"
        result = chunk(text, 11)
        expected = ("A line", "breaking experience")
        self.assert_equal(result, expected)

    def test_breaks_and_removes_custom_multichar_whitespaces(self):
        text = "A line__breaking experience"
        result = chunk(text, 11, whitespaces={"__"})
        expected = ("A line", "breaking experience")
        self.assert_equal(result, expected)

    def test_breaks_at_existing_hyphen(self):
        text = "A line-breaking experience"
        result = chunk(text, 11)
        expected = ("A line-", "breaking experience")
        self.assert_equal(result, expected)

    def test_forces_break(self):
        text = "SomeLongWord"
        result = chunk(text, 5)
        expected = ("Some-", "LongWord")
        self.assert_equal(result, expected)

    def test_breaks_at_existing_soft_hyphen(self):
        text = "A line breaking ex·perience"
        result = chunk(text, 21)
        expected = ("A line breaking ex-", "perience")
        self.assert_equal(result, expected)

    def test_breaks_at_custom_hyphenation_character(self):
        text = "SomeLongWord"
        result = chunk(text, 5, hyphen="0")
        expected = ("Some0", "LongWord")
        self.assert_equal(result, expected)

    def test_does_not_count_soft_hyphens_against_full_width(self):
        text = "·····Hello"
        result = chunk(text, 5)
        expected = ("·····Hello", "")
        self.assert_equal(result, expected)

    def test_does_not_count_soft_hyphens_when_breaking_at_index(self):
        text = "·····He·llo"
        result = chunk(text, 3)
        expected = ("·····He-", "llo")
        self.assert_equal(result, expected)

    def test_breaks_at_multichar_soft_hyphen(self):
        text = "He··llo"
        result = chunk(text, 3, soft_hyphen="··")
        expected = ("He-", "llo")
        self.assert_equal(result, expected)

    def test_breaks_at_multichar_hyphen(self):
        text = "He--llo"
        result = chunk(text, 3, hyphens={"--"})
        expected = ("He--", "llo")
        self.assert_equal(result, expected)


class TestBreakLines(TestCase):
    def test_fills_broken_line(self):
        text = "A truly line breaking experience,\nfulfilling and rewarding."
        result = break_lines(text, width=25)
        expected = [
            "A truly line breaking",
            "experience, fulfilling",
            "and rewarding.",
        ]
        self.assert_equal(result, expected)
