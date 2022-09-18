import string
import unittest
from unittest import mock

import readchar

from . import InputContext, MockException, PrintCall, cutie, yield_input

print_call = PrintCall(
    {
        "selectable": "\x1b[K\x1b[1m( )\x1b[0m ",
        "selected": "\x1b[K\x1b[1m(\x1b[32mx\x1b[0;1m)\x1b[0m ",
        "caption": "\x1b[K",
        "active": "\x1b[K\x1b[32;1m{ }\x1b[0m ",
        "active-selected": "\x1b[K\x1b[32;1m{x}\x1b[0m ",
        "confirm": ("\x1b[1m(( confirm ))\x1b[0m \x1b[K", {"end": "", "flush": True}),
        "confirm-active": (
            "\x1b[1;32m{{ confirm }}\x1b[0m \x1b[K",
            {"end": "", "flush": True},
        ),
        "no_confirm_line": ("\033[K", {"end": "", "flush": True}),
    }
)


PRINT_CALL_END = (("\r\x1b[K",), {"end": "", "flush": True})


class TestSelectMultiplePrint(unittest.TestCase):
    @mock.patch("cutie.print", side_effect=MockException)
    def test_list_newlines(self, mock_print):
        args_list = ["foo", "bar"]
        with self.assertRaises(MockException):
            cutie.select_multiple(args_list)
        mock_print.assert_called_once_with("\n" * (len(args_list) - 1))

    @mock.patch("cutie.readchar.readkey", side_effect=MockException)
    @mock.patch("cutie.print")
    def test_move_to_first_item(self, mock_print, *m):
        args_list = ["foo", "bar"]
        with self.assertRaises(MockException):
            cutie.select_multiple(args_list)
        self.assertEqual(
            mock_print.call_args_list[1], ((f"\033[{len(args_list) + 1}A",),)
        )

    @mock.patch("cutie.readchar.readkey", side_effect=MockException)
    @mock.patch("cutie.print")
    def test_print_options(self, mock_print, *m):
        args_list = ["foo", "bar"]
        expected_calls = [
            print_call("foo", "active"),
            print_call("bar", "selectable"),
            print_call(state="confirm"),
        ]
        with self.assertRaises(MockException):
            cutie.select_multiple(args_list)

    @mock.patch("cutie.readchar.readkey", side_effect=MockException)
    @mock.patch("cutie.print")
    def test_print_options_caption_indices(self, mock_print, *m):
        args_list = ["foo", "bar"]
        expected_calls = [
            print_call("foo", "caption"),
            print_call("bar"),
            print_call(state="no_confirm_line"),
        ]
        with self.assertRaises(MockException):
            cutie.select_multiple(args_list, caption_indices=[0])
        self.assertEqual(mock_print.call_args_list[-3:], expected_calls)

    @mock.patch("cutie.readchar.readkey", side_effect=MockException)
    @mock.patch("cutie.print")
    def test_print_options_selected(self, mock_print, *m):
        args_list = ["foo", "bar"]
        expected_calls = [
            print_call("foo"),
            print_call("bar", "active"),
            print_call(state="no_confirm_line"),
        ]
        with self.assertRaises(MockException):
            cutie.select_multiple(args_list, cursor_index=1)
        self.assertEqual(mock_print.call_args_list[-3:], expected_calls)

    @mock.patch("cutie.readchar.readkey", side_effect=MockException)
    @mock.patch("cutie.print")
    def test_print_options_selected_and_ticked(self, mock_print, *m):
        args_list = ["foo", "bar"]
        expected_calls = [
            print_call("foo", "active-selected"),
            print_call("bar"),
            print_call(state="no_confirm_line"),
        ]
        with self.assertRaises(MockException):
            cutie.select_multiple(args_list, ticked_indices=[0])
        self.assertEqual(mock_print.call_args_list[-3:], expected_calls)

    @mock.patch("cutie.readchar.readkey", side_effect=MockException)
    @mock.patch("cutie.print")
    def test_print_options_deselected_unticked(self, mock_print, *m):
        args_list = ["foo", "bar"]
        expected_calls = [
            print_call("foo"),
            print_call("bar"),
            print_call(state="no_confirm_line"),
        ]
        with self.assertRaises(MockException):
            cutie.select_multiple(args_list, cursor_index=2)
        self.assertEqual(mock_print.call_args_list[-3:], expected_calls)

    @mock.patch("cutie.readchar.readkey", side_effect=MockException)
    @mock.patch("cutie.print")
    def test_print_deselected_confirm(self, mock_print, *m):
        expected_call = print_call(state="confirm")
        with self.assertRaises(MockException):
            cutie.select_multiple([], cursor_index=1, hide_confirm=False)
        self.assertEqual(mock_print.call_args_list[-1], expected_call)

    @mock.patch("cutie.readchar.readkey", side_effect=MockException)
    @mock.patch("cutie.print")
    def test_print_selected_confirm(self, mock_print, *m):
        expected_call = print_call(state="confirm-active")
        with self.assertRaises(MockException):
            cutie.select_multiple([], hide_confirm=False)
        self.assertEqual(mock_print.call_args_list[-1], expected_call)

    @mock.patch("cutie.readchar.readkey", side_effect=MockException)
    @mock.patch("cutie.print")
    def test_print_show_confirm(self, mock_print, *m):
        expected_calls = [print_call("foo", "active"), print_call(state="confirm")]
        with self.assertRaises(MockException):
            cutie.select_multiple(["foo"], hide_confirm=False)
        self.assertEqual(mock_print.call_args_list[2:], expected_calls)


class TestSelectMultipleMoveAndSelect(unittest.TestCase):
    @mock.patch("cutie.print")
    def test_move_up(self, mock_print):
        call_args = ["foo", "bar"]
        expected_calls = [
            print_call("foo", "active"),
            print_call("bar"),
            print_call(state="no_confirm_line"),
            PRINT_CALL_END,
        ]
        with InputContext(readchar.key.UP, readchar.key.ENTER):
            cutie.select_multiple(call_args, cursor_index=1)
        self.assertEqual(mock_print.call_args_list[-4:], expected_calls)

    @mock.patch("cutie.print")
    def test_move_up_skip_caption(self, mock_print):
        call_args = ["foo", "bar", "baz"]
        expected_calls = [
            print_call("foo", "active"),
            print_call("bar", "caption"),
            print_call("baz"),
            print_call(state="no_confirm_line"),
            PRINT_CALL_END,
        ]
        with InputContext(readchar.key.UP, readchar.key.ENTER):
            cutie.select_multiple(call_args, cursor_index=2, caption_indices=[1])
        self.assertEqual(mock_print.call_args_list[-5:], expected_calls)

    @mock.patch("cutie.print")
    def test_move_down(self, mock_print):
        call_args = ["foo", "bar"]
        expected_calls = [
            print_call("foo"),
            print_call("bar", "active"),
            print_call(state="no_confirm_line"),
            PRINT_CALL_END,
        ]
        with InputContext(readchar.key.DOWN, readchar.key.ENTER):
            cutie.select_multiple(call_args)
        self.assertEqual(mock_print.call_args_list[-4:], expected_calls)

    @mock.patch("cutie.print")
    def test_move_down_skip_caption(self, mock_print):
        call_args = ["foo", "bar", "baz"]
        expected_calls = [
            print_call("foo"),
            print_call("bar", "caption"),
            print_call("baz", "active"),
            print_call(state="no_confirm_line"),
            PRINT_CALL_END,
        ]
        with InputContext(readchar.key.DOWN, readchar.key.ENTER):
            cutie.select_multiple(call_args, caption_indices=[1])
        self.assertEqual(mock_print.call_args_list[-5:], expected_calls)

    @mock.patch("cutie.print")
    def test_select(self, mock_print):
        call_args = ["foo", "bar"]
        expected_calls = [
            print_call("foo", "selected"),
            print_call("bar", "active-selected"),
            print_call(state="no_confirm_line"),
            PRINT_CALL_END,
        ]
        with InputContext(" ", readchar.key.DOWN, " ", readchar.key.ENTER):
            selected_indices = cutie.select_multiple(call_args)
        self.assertEqual(mock_print.call_args_list[-4:], expected_calls)
        self.assertEqual(selected_indices, [0, 1])

    @mock.patch("cutie.print")
    def test_select_min_too_few(self, mock_print):
        call_args = ["foo"]
        expected_call = (
            ("Must select at least 1 options\x1b[K",),
            {"end": "", "flush": True},
        )
        with InputContext(readchar.key.DOWN, readchar.key.ENTER):
            with self.assertRaises(MockException):
                cutie.select_multiple(call_args, minimal_count=1)
            self.assertEqual(mock_print.call_args_list[-1], expected_call)

    @mock.patch("cutie.print")
    def test_select_max_too_many(self, mock_print):
        call_args = ["foo"]
        expected_call = (
            ("Must select at most 0 options\x1b[K",),
            {"end": "", "flush": True},
        )
        with InputContext(readchar.key.ENTER):
            with self.assertRaises(MockException):
                cutie.select_multiple(call_args, maximal_count=0, ticked_indices=[0])
            self.assertEqual(mock_print.call_args_list[-1], expected_call)

    @mock.patch("cutie.print")
    def test_select_min_sufficient(self, mock_print):
        call_args = ["foo"]
        expected_calls = [
            print_call("foo", "active-selected"),
            print_call(state="no_confirm_line"),
            PRINT_CALL_END,
        ]
        with InputContext(" ", readchar.key.ENTER):
            selected_indices = cutie.select_multiple(call_args, minimal_count=1)
            self.assertEqual(mock_print.call_args_list[-3:], expected_calls)
            self.assertEqual(selected_indices, [0])

    @mock.patch("cutie.print")
    def test_deselect_on_min_sufficient(self, mock_print):
        call_args = ["foo", "bar"]
        expected_calls = [
            print_call("foo", "selectable"),
            print_call("bar", "active-selected"),
            print_call(state="no_confirm_line"),
            PRINT_CALL_END,
        ]
        with InputContext(" ", readchar.key.DOWN, readchar.key.ENTER):
            selected_indices = cutie.select_multiple(
                call_args, minimal_count=1, ticked_indices=[0, 1]
            )
            self.assertEqual(mock_print.call_args_list[-4:], expected_calls)
            self.assertEqual(selected_indices, [1])

    @mock.patch("cutie.print")
    def test_select_max_okay(self, mock_print):
        call_args = ["foo"]
        expected_calls = [
            print_call("foo", "active-selected"),
            print_call(state="no_confirm_line"),
            PRINT_CALL_END,
        ]
        with InputContext(" ", readchar.key.ENTER):
            selected_indices = cutie.select_multiple(call_args, maximal_count=1)
            self.assertEqual(mock_print.call_args_list[-3:], expected_calls)
            self.assertEqual(selected_indices, [0])

    @mock.patch("cutie.print")
    def test_select_min_too_few_hide_confirm(self, mock_print):
        """
        This should prompt the user with an error message
        """
        call_args = ["foo"]
        expected_call = (
            ("Must select at least 1 options\x1b[K",),
            {"end": "", "flush": True},
        )
        with InputContext(readchar.key.ENTER):
            with self.assertRaises(MockException):
                cutie.select_multiple(call_args, minimal_count=1)
            self.assertEqual(mock_print.call_args_list[-1], expected_call)

    @mock.patch("cutie.print")
    def test_select_max_too_many_show_confirm(self, mock_print):
        """
        This should prompt the user with an error message
        """
        call_args = ["foo"]
        expected_call = (
            ("\x1b[1;32m{{ confirm }}\x1b[0m Must select at most 0 options\x1b[K",),
            {"end": "", "flush": True},
        )
        with InputContext(readchar.key.DOWN, readchar.key.ENTER):
            with self.assertRaises(MockException):
                cutie.select_multiple(
                    call_args, maximal_count=0, ticked_indices=[0], hide_confirm=False
                )
            self.assertEqual(mock_print.call_args_list[-1], expected_call)


class TestSelectMultipleMisc(unittest.TestCase):
    @mock.patch("cutie.print")
    def test_keyboard_interrupt(self, mock_print):
        call_args = ["foo", "bar"]
        with InputContext(readchar.key.CTRL_C):
            with self.assertRaises(KeyboardInterrupt):
                cutie.select_multiple(call_args)
