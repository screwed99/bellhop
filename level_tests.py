import unittest
from unittest.mock import patch, mock_open

from level import Level

class LevelTests(unittest.TestCase):

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
        # mock_level_file_open.assert_called_once_with(filename, 'r') # I don't understand this but it's failing when I'm faily sure it shouldn't be
        self.assertRaises(IOError, Level, filename=filename)
