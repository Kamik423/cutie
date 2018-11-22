import unittest
from unittest import mock
import string

from . import MockException, InputContext, PrintCall, cutie

import readchar


print_call = PrintCall({
                            'selectable': '\x1b[K\x1b[1m[ ]\x1b[0m ',
                            'selected': '\x1b[K\x1b[1m[\x1b[32;1mx\x1b[0;1m]\x1b[0m ',
                            'caption': '\x1b[K'
})


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
        expected_calls = [
                            print_call("foo", "selected"),
                            print_call("bar")
        ]
        with self.assertRaises(MockException):
            cutie.select(args_list)
        self.assertEqual(mock_print.call_args_list[2:], expected_calls)


    @mock.patch("cutie.readchar.readkey", side_effect=MockException)
    @mock.patch("cutie.print")
    def test_print_options_selected_index_set(self, mock_print, *m):
        args_list = ["foo", "bar"]
        expected_calls = [
                            print_call("foo"),
                            print_call("bar", "selected")
        ]
        with self.assertRaises(MockException):
            cutie.select(args_list, selected_index=1)
        self.assertEqual(mock_print.call_args_list[2:], expected_calls)

    @mock.patch("cutie.readchar.readkey", side_effect=MockException)
    @mock.patch("cutie.print")
    def test_print_non_selectable(self, mock_print, *m):
        args_list = ["foo", "bar"]
        expected_calls = [
                            print_call("foo", "selected"),
                            print_call("bar", "caption")
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
    def test_ignore_unrecognized_key(self, mock_print):
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
                    'DOWN',
                    'ENTER',
                    'CTRL_C',
                    'CTRL_D'
                    ]
        all_keys = [getattr(readchar.key, k) for k in dir(readchar.key) if k not in exclude]
        all_keys.extend(string.printable)
        expected_calls = [
                            (('',),),
                            (('\x1b[2A',),),
                            (('\x1b[K\x1b[1m[\x1b[32;1mx\x1b[0;1m]\x1b[0m foo',),),
                        ]

        for key in all_keys:
            with InputContext(readchar.key.DOWN, key, readchar.key.ENTER):
                selindex = cutie.select(["foo"])
                self.assertEqual(selindex, 0)
                self.assertEqual(mock_print.call_args_list[:3], expected_calls)
                mock_print.reset_mock()

    @mock.patch("cutie.print")
    def test_move_up(self, *m):
        with InputContext(readchar.key.UP, "\r"):
            args_list = ["foo", "bar"]
            selindex = cutie.select(args_list, selected_index=1)
            self.assertEqual(selindex, 0)

    @mock.patch("cutie.print")
    def test_move_up_skip_caption(self, *m):
        with InputContext(readchar.key.UP, "\r"):
            args_list = ["foo", "bar", "baz"]
            selindex = cutie.select(args_list, selected_index=2, caption_indices=[1])
            self.assertEqual(selindex, 0)

    @mock.patch("cutie.print")
    def test_move_down(self, *m):
        with InputContext(readchar.key.DOWN, "\r"):
            args_list = ["foo", "bar"]
            selindex = cutie.select(args_list)
            self.assertEqual(selindex, 1)

    @mock.patch("cutie.print")
    def test_move_down_skip_caption(self, *m):
        with InputContext(readchar.key.DOWN, "\r"):
            args_list = ["foo", "bar", "baz"]
            selindex = cutie.select(args_list, caption_indices=[1])
            self.assertEqual(selindex, 2)

    @mock.patch("cutie.print")
    def test_keyboard_interrupt_ctrl_c_no_input(self, *m):
        with InputContext(readchar.key.CTRL_C):
            with self.assertRaises(KeyboardInterrupt):
                cutie.select(["foo"])

    @mock.patch("cutie.print")
    def test_keyboard_interrupt_ctrl_c_selected(self, *m):
        with InputContext(readchar.key.DOWN, readchar.key.CTRL_C):
            with self.assertRaises(KeyboardInterrupt):
                cutie.select(["foo"], selected_index=0)

    @mock.patch("cutie.print")
    def test_keyboard_interrupt_ctrl_d_no_input(self, *m):
        with InputContext(readchar.key.CTRL_D):
            with self.assertRaises(KeyboardInterrupt):
                cutie.select(["foo"])

    @mock.patch("cutie.print")
    def test_keyboard_interrupt_ctrl_d_selected(self, *m):
        with InputContext(readchar.key.DOWN, readchar.key.CTRL_D):
            with self.assertRaises(KeyboardInterrupt):
                cutie.select(["foo"], selected_index=0)
