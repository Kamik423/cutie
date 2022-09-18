import unittest
from unittest import mock

import cutie


class TestSecureInput(unittest.TestCase):
    def test_secure_input(self):
        with mock.patch("cutie.getpass.getpass", return_value="foo") as mock_getpass:
            self.assertEqual(cutie.secure_input("foo"), "foo")
            mock_getpass.assert_called_once_with("foo ")
