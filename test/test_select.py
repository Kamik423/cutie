import unittest
from unittest import mock
import string

from . import MockException, yield_input

import readchar

import cutie


class TestSelect(unittest.TestCase):

    @mock.patch("cutie.print", side_effect=MockException)
    def test_print_list_newlines(self, mock_print):
        args_list = ["foo", "bar"]
        with self.assertRaises(MockException):
            cutie.select(args_list)
            mock_print.assert_called_once_with("\n" * (len(args_list) - 1))

    @mock.patch("cutie.readchar.readkey", side_effect=MockException)
    @mock.patch("cutie.print")
    def test_print_move_to_first_item(self, mock_print, *m):
        args_list = ["foo", "bar"]
        with self.assertRaises(MockException):
            cutie.select(args_list)
            self.assertEqual(mock_print.call_args_list[1], ((f"\033[{len(args_list) + 1}A",),))

    @mock.patch("cutie.readchar.readkey", side_effect=MockException)
    @mock.patch("cutie.print")
    def test_print_options(self, mock_print, *m):
        args_list = ["foo", "bar"]
        expected_calls =  [
                            (('\x1b[K\x1b[1m[\x1b[32;1mx\x1b[0;1m]\x1b[0m foo',),),
                            (('\x1b[K\x1b[1m[ ]\x1b[0m bar',),),
                        ]
        with self.assertRaises(MockException):
            cutie.select(args_list)
            self.assertEqual(mock_print.call_args_list[2:], expected_calls)

    @mock.patch("cutie.readchar.readkey", side_effect=MockException)
    @mock.patch("cutie.print")
    def test_print_options_selected_index_set(self, mock_print, *m):
        args_list = ["foo", "bar"]
        expected_calls =  [
                            (('\x1b[K\x1b[1m[ ]\x1b[0m foo',),),
                            (('\x1b[K\x1b[1m[\x1b[32;1mx\x1b[0;1m]\x1b[0m bar',),),
                        ]
        with self.assertRaises(MockException):
            cutie.select(args_list, selected_index=1)
            self.assertEqual(mock_print.call_args_list[2:], expected_calls)

    @mock.patch("cutie.readchar.readkey", side_effect=MockException)
    @mock.patch("cutie.print")
    def test_print_non_selectable(self, mock_print, *m):
        args_list = ["foo", "bar"]
        expected_calls =  [
                            (('\x1b[K\x1b[1m[\x1b[32;1mx\x1b[0;1m]\x1b[0m foo',),),
                            (('\x1b[Kbar',),)
                        ]
        with self.assertRaises(MockException):
            cutie.select(args_list, caption_indices=[1])
            self.assertEqual(mock_print.call_args_list[2:], expected_calls)

    @mock.patch("cutie.readchar.readkey", side_effect=MockException)
    @mock.patch("cutie.print")
    def test_print_options_custom_prefixes(self, mock_print, *m):
        args_list = ["foo", "bar", "baz"]
        expected_calls =  [
                            (('\x1b[K*foo',),),
                            (('\x1b[K+bar',),),
                            (('\x1b[K$baz',),)
                        ]
        with self.assertRaises(MockException):
            cutie.select(
                            args_list,
                            caption_indices=[2],
                            selected_prefix="*",
                            deselected_prefix="+",
                            caption_prefix="$"
                        )
            self.assertEqual(mock_print.call_args_list[2:], expected_calls)

    @mock.patch("cutie.print")
    def test_exit_on_unrecognized_key(self, *m):
        exclude = [
                    '__builtins__',
                    '__cached__',
                    '__doc__',
                    '__file__',
                    '__loader__',
                    '__name__',
                    '__package__',
                    '__spec__',
                    'UP',
                    'DOWN'
                    ]
        all_keys = [getattr(readchar.key, k) for k in dir(readchar.key) if k not in exclude]
        all_keys.extend(string.printable)
        for key in all_keys:
            cutie.readchar.readkey = yield_input(readchar.key.DOWN, key)
            selindex = cutie.select(["foo", "bar"])
            self.assertEqual(selindex, 1)

    @mock.patch("cutie.print")
    def test_move_up(self, *m):
        cutie.readchar.readkey = yield_input(readchar.key.UP, "\r")
        args_list = ["foo", "bar"]
        selindex = cutie.select(args_list, selected_index=1)
        self.assertEqual(selindex, 0)

    @mock.patch("cutie.print")
    def test_move_up_skip_caption(self, *m):
        cutie.readchar.readkey = yield_input(readchar.key.UP, "\r")
        args_list = ["foo", "bar", "baz"]
        selindex = cutie.select(args_list, selected_index=2, caption_indices=[1])
        self.assertEqual(selindex, 0)

    @mock.patch("cutie.print")
    def test_move_down(self, *m):
        cutie.readchar.readkey = yield_input(readchar.key.DOWN, "\r")
        args_list = ["foo", "bar"]
        selindex = cutie.select(args_list)
        self.assertEqual(selindex, 1)

    @mock.patch("cutie.print")
    def test_move_down_skip_caption(self, *m):
        cutie.readchar.readkey = yield_input(readchar.key.DOWN, "\r")
        args_list = ["foo", "bar", "baz"]
        selindex = cutie.select(args_list, caption_indices=[1])
        self.assertEqual(selindex, 2)
