"""Unittests for utils class."""
import unittest
from scrolltext.utils import CharacterScroller, parse_int


class CharacterScrollTests(unittest.TestCase):
    """Test cases for CharacterScroller class"""

    def test_invalid_params1(self):
        """"Test creation of CharacterScroller with no parameters."""
        with self.assertRaises(Exception):
            CharacterScroller()

    def test_dunno_visible_text_length_is_zero(self):
        """"Test with visibile window size set to 0."""
        cnt = 0
        scroll_text = "Hello, world"
        for text in CharacterScroller(0, 1, scroll_text):
            self.assertEqual("", text)
            cnt += 1
        self.assertEqual(cnt, len(scroll_text) + 2)

    def test_scroll_character_for_character(self):
        """"Test with visibile window size set to 1, or character by
        character respectively."""
        scroll_text = "Hello, world"
        expected = list(scroll_text)
        cnt = 0
        for text in CharacterScroller(1, 0, scroll_text):
            self.assertEqual(expected[cnt], text)
            cnt += 1
        self.assertEqual(cnt, len(scroll_text))

    def test_scroll_character_for_character_with_spaces(self):
        """"Test with visibile window size set to 1, and a leading
        and trailing blank character."""
        scroll_text = "Hello, world"
        scroll_text2 = " " + scroll_text + " "
        expected = list(scroll_text2)
        cnt = 0
        for text in CharacterScroller(1, 1, scroll_text):
            self.assertEqual(expected[cnt], text)
            cnt += 1
        self.assertEqual(cnt, len(scroll_text) + 2)

    def test_scroll_two_characters_with_spaces(self):
        """"Test with visibile window size set to two, or two chars at a time."""
        scroll_text = "Hello, world"
        expected = [" H", "He", "el", "ll", "lo", "o,", ", ", " w", "wo", "or",
                    "rl", "ld", "d ", " "]
        cnt = 0
        for text in CharacterScroller(2, 1, scroll_text):
            self.assertEqual(expected[cnt], text)
            cnt += 1
        self.assertEqual(cnt, len(scroll_text) + 2)

    def test_scroll_in_broad_window_with_spaces(self):
        """"Test with a much larger window size, than the given text."""
        scroll_text = "Hello, world"
        expected = [" Hello, world ", "Hello, world ", "ello, world ", "llo, world ",
                    "lo, world ", "o, world ", ", world ", " world ", "world ",
                    "orld ", "rld ", "ld ", "d ", " "]
        cnt = 0
        for text in CharacterScroller(80, 1, scroll_text):
            self.assertEqual(expected[cnt], text)
            cnt += 1
        self.assertEqual(cnt, len(scroll_text) + 2)

    def test_scroll_character_for_character_right_to_left2(self):
        """"Right-to-Left text. Test with visibile window size set to 1, or character by
        character respectively."""
        scroll_text_list = list("Hello, world")
        scroll_text_list.reverse()
        scroll_text = "".join(scroll_text_list)
        print("orig", scroll_text)
        expected = list(scroll_text)
        expected.reverse()
        print("copy", expected)
        cnt = 0
        for text in CharacterScroller(1, 0, scroll_text, 1):
            print("round", str(cnt))
            try:
                self.assertEqual(expected[cnt], text)
            except IndexError:
                pass
            cnt += 1
        self.assertTrue(((cnt + len(scroll_text)) // 2) == len(scroll_text))

    def test_scroll_character_for_character_right_to_left(self):
        """"Right-to-Left text. Test with visibile window size set to 1, or character by
        character respectively."""
        scroll_text = "مرحباً فيلت"
        expected = list(scroll_text)
        expected.reverse()
        cnt = 0
        for text in CharacterScroller(1, 0, scroll_text, 1):
            print("round", str(cnt), " ", text)
            try:
                self.assertEqual(expected[cnt], text)
            except IndexError:
                pass
            cnt += 1
        self.assertTrue(((cnt + len(scroll_text)) // 2) == len(scroll_text))


class ParseIntTests(unittest.TestCase):
    """Test cases for parse int utility"""
    def test_parse_none_returns_0(self):
        """Given None returns 0"""
        self.assertEqual(parse_int(None), 0)

    def test_parse_empty_str_returns_0(self):
        """Given empty str returns 0"""
        self.assertEqual(parse_int(""), 0)

    def test_parse_str1_returns_int1(self):
        """Given "1" returns 1"""
        self.assertEqual(parse_int("1"), 1)

    def test_parse_str_minus1_returns_int_minus1(self):
        """Given "-1" returns -1"""
        self.assertEqual(parse_int("-1"), -1)


if __name__ == '__main__':
    unittest.main()
