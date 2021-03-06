import unittest
from unittest.mock import patch, mock_open

from levels.level_parser import LevelParser


class LevelParserTests(unittest.TestCase):

    _text_moves_out_of_order = """
level 1 5 5 3
1:{0:[1]}
0:{1:[2]}
end_level
"""

    @patch("builtins.open", new_callable=mock_open, read_data=_text_moves_out_of_order)
    def test__get_next_event__moves_out_of_order__throws_exception(self, mock_level_file_open):

        # These two lines are pure garbage and wouldn't be needed if we updated to Python 3.7
        # Details: https://bugs.python.org/issue32933
        mock_level_file_open.return_value.__iter__ = lambda self: self
        mock_level_file_open.return_value.__next__ = lambda self: next(iter(self.readline, ''))

        filename = "filename.txt"
        level_parser = LevelParser(filename)

        self.assertRaises(IOError, level_parser.parse_from_file)

        mock_level_file_open.assert_called_once_with(filename, 'r')
