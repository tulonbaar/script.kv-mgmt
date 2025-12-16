import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# We need to mock sys.stdin and termios/tty for input_with_esc
# Since input_with_esc is in main.py, we import it.
# But main.py has global code that runs on import?
# main.py has `if __name__ == "__main__": main_menu()` so it should be safe to import.

from main import input_with_esc

class TestInputEsc(unittest.TestCase):

    @patch('sys.stdin.fileno')
    @patch('termios.tcgetattr')
    @patch('termios.tcsetattr')
    @patch('tty.setcbreak')
    @patch('sys.stdin.read')
    @patch('sys.stdout.write')
    def test_input_esc_linux(self, mock_write, mock_read, mock_setcbreak, mock_tcsetattr, mock_tcgetattr, mock_fileno):
        # Simulate Linux environment
        with patch('os.name', 'posix'):
            # Simulate pressing Esc (27)
            mock_read.side_effect = [chr(27)]
            
            result = input_with_esc("Prompt: ")
            
            self.assertIsNone(result)
            mock_write.assert_any_call("Prompt: ")

    @patch('sys.stdin.fileno')
    @patch('termios.tcgetattr')
    @patch('termios.tcsetattr')
    @patch('tty.setcbreak')
    @patch('sys.stdin.read')
    @patch('sys.stdout.write')
    def test_input_text_linux(self, mock_write, mock_read, mock_setcbreak, mock_tcsetattr, mock_tcgetattr, mock_fileno):
        # Simulate Linux environment
        with patch('os.name', 'posix'):
            # Simulate typing 'a', 'b', Enter (10)
            mock_read.side_effect = ['a', 'b', chr(10)]
            
            result = input_with_esc("Prompt: ")
            
            self.assertEqual(result, "ab")
            # Verify 'a' and 'b' were echoed
            mock_write.assert_any_call('a')
            mock_write.assert_any_call('b')

if __name__ == '__main__':
    unittest.main()
