from uneedtest import TestCase

from tamal.wrap import wrap


class TestWrap(TestCase):
    def test_respects_paragraphs(self):
        target_width = 64
        text = (
            "This is a paragraph."
            "\n\n"  # paragraph should be preserved
            "Here comes a second paragraph, but this one is a little longer"
            " and it contains a linebreak\n"
            "which should not be in the output. And this text is just for "
            "checking linebreaking."
        )
        result = wrap(text, width=target_width)
        expected_lines = [
            "This is a paragraph.",
            "",
            "Here comes a second paragraph, but this one is a little longer",
            "and it contains a linebreak which should not be in the output.",
            "And this text is just for checking linebreaking.",
        ]
        assert all(len(line) <= target_width for line in expected_lines)
        expected = "\n".join(expected_lines)
        self.assert_equal(result, expected)

    def test_respects_custom_paragraph_marker(self):
        target_width = 64
        paragraph_marker = "****"
        text = (
            "This is a paragraph."
            f"{paragraph_marker}"  # paragraph marker should result in paragraph
            "Here comes a second paragraph, but this one is a little longer"
            " and it contains a linebreak\n"
            "which should not be in the output. And this text is just for "
            "checking linebreaking."
        )
        result = wrap(text, width=target_width, paragraph=paragraph_marker)
        expected_lines = [
            "This is a paragraph.",
            "",
            "Here comes a second paragraph, but this one is a little longer",
            "and it contains a linebreak which should not be in the output.",
            "And this text is just for checking linebreaking.",
        ]
        assert all(len(line) <= target_width for line in expected_lines)
        expected = "\n".join(expected_lines)
        self.assert_equal(result, expected)
