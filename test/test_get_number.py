import unittest
from unittest import mock

import cutie

from . import MockException


class TestCutieGetNumber(unittest.TestCase):
    @mock.patch("cutie.print", side_effect=MockException)
    def test_invalid_number(self, mock_print):
        with mock.patch("cutie.input", return_value="foo"):
            with self.assertRaises(MockException):
                cutie.get_number("bar")
            mock_print.assert_called_once_with(
                "Not a valid number.\033[K\033[1A\r\033[K", end=""
            )

    @mock.patch("cutie.print", side_effect=MockException)
    def test_not_allow_float(self, mock_print):
        with mock.patch("cutie.input", return_value="1.2"):
            with self.assertRaises(MockException):
                cutie.get_number("foo", allow_float=False)
            mock_print.assert_called_once_with(
                "Has to be an integer.\033[K\033[1A\r\033[K", end=""
            )

    def test_allow_float_returns_float(self):
        with mock.patch("cutie.input", return_value="1.2"):
            val = cutie.get_number("foo")
            self.assertIsInstance(val, float)
            self.assertEqual(val, 1.2)

    def test_not_allow_float_returns_int(self):
        with mock.patch("cutie.input", return_value="1"):
            val = cutie.get_number("foo", allow_float=False)
            self.assertIsInstance(val, int)
            self.assertEqual(val, 1)

    @mock.patch("cutie.print", side_effect=MockException)
    def test_min_value_float_too_low(self, mock_print):
        with mock.patch("cutie.input", return_value="1.2"):
            with self.assertRaises(MockException):
                cutie.get_number("foo", min_value=1.3)
            mock_print.assert_called_once_with(
                "Has to be at least 1.3.\033[K\033[1A\r\033[K", end=""
            )

    def test_min_value_float_equal(self):
        with mock.patch("cutie.input", return_value="1.2"):
            self.assertEqual(cutie.get_number("foo", min_value=1.2), 1.2)

    def test_min_value_float_greater(self):
        with mock.patch("cutie.input", return_value="1.3"):
            self.assertEqual(cutie.get_number("foo", min_value=1.2), 1.3)

    @mock.patch("cutie.print", side_effect=MockException)
    def test_min_value_int_too_low(self, mock_print):
        with mock.patch("cutie.input", return_value="1"):
            with self.assertRaises(MockException):
                cutie.get_number("foo", min_value=2)
            mock_print.assert_called_once_with(
                "Has to be at least 2.\033[K\033[1A\r\033[K", end=""
            )

    def test_min_value_int_equal(self):
        with mock.patch("cutie.input", return_value="1"):
            self.assertEqual(cutie.get_number("foo", min_value=1), 1)

    def test_min_value_int_greater(self):
        with mock.patch("cutie.input", return_value="2"):
            self.assertEqual(cutie.get_number("foo", min_value=1), 2)

    @mock.patch("cutie.print", side_effect=MockException)
    def test_max_value_float_too_high(self, mock_print):
        with mock.patch("cutie.input", return_value="1.2"):
            with self.assertRaises(MockException):
                cutie.get_number("foo", max_value=1.1)
            mock_print.assert_called_once_with(
                "Has to be at most 1.1.\033[1A\r\033[K", end=""
            )

    def test_max_value_float_equal(self):
        with mock.patch("cutie.input", return_value="1.1"):
            self.assertEqual(cutie.get_number("foo", max_value=1.1), 1.1)

    def test_max_value_float_smaller(self):
        with mock.patch("cutie.input", return_value="1.1"):
            self.assertEqual(cutie.get_number("foo", max_value=1.2), 1.1)

    @mock.patch("cutie.print", side_effect=MockException)
    def test_max_value_int_too_high(self, mock_print):
        with mock.patch("cutie.input", return_value="2"):
            with self.assertRaises(MockException):
                cutie.get_number("foo", max_value=1)
            mock_print.assert_called_once_with(
                "Has to be at most 1.\033[1A\r\033[K", end=""
            )

    def test_max_value_int_equal(self):
        with mock.patch("cutie.input", return_value="1"):
            self.assertEqual(cutie.get_number("foo", max_value=1), 1)

    def test_max_value_int_smaller(self):
        with mock.patch("cutie.input", return_value="1"):
            self.assertEqual(cutie.get_number("foo", max_value=2), 1)

    @mock.patch("cutie.print")
    def test_print_finalize(self, mock_print):
        with mock.patch("cutie.input", return_value="1"):
            cutie.get_number("foo")
        mock_print.assert_called_once_with("\033[K", end="")
