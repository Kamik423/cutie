import unittest
from unittest import mock

import readchar

from . import InputContext, MockException, PrintCall, cutie

print_call = PrintCall(
    {
        "selected": "\x1b[K\x1b[31m>\x1b[0m ",
        "selectable": "\x1b[K  ",
    }
)


class TestPromtYesOrNo(unittest.TestCase):

    default_yes_print_calls = [
        (tuple(),),
        (("\x1b[K\x1b[31m>\x1b[0m Yes",),),
        (("\x1b[K  No",),),
        (("\x1b[3A\r\x1b[Kfoo (Y/N) Yes",), {"end": "", "flush": True}),
        (("\x1b[K\n\x1b[K\n\x1b[K\n\x1b[3A",),),
    ]

    default_no_print_calls = [
        (tuple(),),
        (("\x1b[K  Yes",),),
        (("\x1b[K\x1b[31m>\x1b[0m No",),),
        (("\x1b[3A\r\x1b[Kfoo (Y/N) No",), {"end": "", "flush": True}),
        (("\x1b[K\n\x1b[K\n\x1b[K\n\x1b[3A",),),
    ]

    @mock.patch("cutie.print")
    def test_print_message(self, mock_print):
        expected_calls = [
            (tuple(),),
            (("\x1b[K  Yes",),),
            (("\x1b[K\x1b[31m>\x1b[0m No",),),
            (
                ("\x1b[3A\r\x1b[Kfoo (Y/N) ",),
                {"end": "", "flush": True},
            ),
            (("\x1b[K\n\x1b[K\n\x1b[K\n\x1b[3A",),),
        ]
        with InputContext(readchar.key.ENTER):
            cutie.prompt_yes_or_no("foo")
            self.assertEqual(mock_print.call_args_list, expected_calls)

    @mock.patch("cutie.print")
    def test_print_message_custom_prefixes(self, mock_print):
        expected_calls = [
            (("\x1b[K+Yes",),),
            (("\x1b[K*No",),),
        ]
        with InputContext(readchar.key.ENTER):
            cutie.prompt_yes_or_no("foo", selected_prefix="*", deselected_prefix="+")
            self.assertEqual(mock_print.call_args_list[1:3], expected_calls)

    @mock.patch("cutie.print")
    def test_print_message_custom_yes_no_text(self, mock_print):
        expected_calls = [
            (("\x1b[K  bar",),),
            (("\x1b[K\x1b[31m>\x1b[0m baz",),),
        ]
        with InputContext(readchar.key.ENTER):
            cutie.prompt_yes_or_no("foo", yes_text="bar", no_text="baz")
            self.assertEqual(mock_print.call_args_list[1:3], expected_calls)

    @mock.patch("cutie.print")
    def test_print_message_default_is_yes(self, mock_print):
        expected_calls = [
            (("\x1b[K\x1b[31m>\x1b[0m Yes",),),
            (("\x1b[K  No",),),
        ]
        with InputContext(readchar.key.ENTER):
            cutie.prompt_yes_or_no("foo", default_is_yes=True)
            self.assertEqual(mock_print.call_args_list[1:3], expected_calls)

    @mock.patch("cutie.print")
    def test_move_up(self, mock_print):
        with InputContext(readchar.key.UP, readchar.key.ENTER):
            self.assertTrue(cutie.prompt_yes_or_no("foo"))
            self.assertEqual(
                mock_print.call_args_list[-5:], self.default_yes_print_calls
            )

    @mock.patch("cutie.print")
    def test_move_up_over_boundary(self, mock_print):
        with InputContext(readchar.key.UP, readchar.key.UP, readchar.key.ENTER):
            self.assertFalse(cutie.prompt_yes_or_no("foo"))
            self.assertEqual(
                mock_print.call_args_list[-5:], self.default_no_print_calls
            )

    @mock.patch("cutie.print")
    def test_move_down(self, mock_print):
        with InputContext(readchar.key.DOWN, readchar.key.ENTER):
            self.assertFalse(cutie.prompt_yes_or_no("foo", default_is_yes=True))
            self.assertEqual(
                mock_print.call_args_list[-5:], self.default_no_print_calls
            )

    @mock.patch("cutie.print")
    def test_move_down_over_boundary(self, mock_print):
        with InputContext(readchar.key.DOWN, readchar.key.ENTER):
            self.assertTrue(cutie.prompt_yes_or_no("foo"))
            self.assertEqual(
                mock_print.call_args_list[-5:], self.default_yes_print_calls
            )

    @mock.patch("cutie.print")
    def test_backspace_delete_char(self, mock_print):
        expected_calls = [
            (tuple(),),
            print_call("Yes", "selected"),
            print_call("No"),
            (
                ("\x1b[3A\r\x1b[Kfoo (Y/N) Ye",),
                {"end": "", "flush": True},
            ),
            (("\x1b[K\n\x1b[K\n\x1b[K\n\x1b[3A",),),
        ]
        with InputContext(readchar.key.UP, readchar.key.BACKSPACE, readchar.key.ENTER):
            cutie.prompt_yes_or_no("foo")
            self.assertEqual(mock_print.call_args_list[-5:], expected_calls)

    @mock.patch("cutie.print")
    def test_ctrl_c_abort(self, *m):
        with InputContext(readchar.key.CTRL_C):
            with self.assertRaises(KeyboardInterrupt):
                cutie.prompt_yes_or_no("")

    @mock.patch("cutie.print")
    def test_ctrl_c_abort_with_input(self, *m):
        with InputContext(readchar.key.UP, readchar.key.CTRL_D):
            with self.assertRaises(KeyboardInterrupt):
                cutie.prompt_yes_or_no("")

    @mock.patch("cutie.print")
    def test_ctrl_d_abort(self, *m):
        with InputContext(readchar.key.CTRL_D):
            with self.assertRaises(KeyboardInterrupt):
                cutie.prompt_yes_or_no("")

    @mock.patch("cutie.print")
    def test_ctrl_d_abort_with_input(self, *m):
        with InputContext(readchar.key.UP, readchar.key.CTRL_D):
            with self.assertRaises(KeyboardInterrupt):
                cutie.prompt_yes_or_no("")

    @mock.patch("cutie.print")
    def test_enter_confirm_default(self, *m):
        with InputContext(readchar.key.ENTER):
            self.assertFalse(cutie.prompt_yes_or_no(""))

    @mock.patch("cutie.print")
    def test_enter_confirm_selection(self, *m):
        with InputContext(readchar.key.UP, readchar.key.ENTER):
            self.assertTrue(cutie.prompt_yes_or_no(""))

    @mock.patch("cutie.print")
    def test_tab_select(self, mock_print):
        expected_calls = [
            (tuple(),),
            print_call("Yes"),
            print_call("No", "selected"),
            (
                ("\x1b[3A\r\x1b[Kfoo (Y/N) No",),
                {"end": "", "flush": True},
            ),
            (("\x1b[K\n\x1b[K\n\x1b[K\n\x1b[3A",),),
        ]
        with InputContext("\t", readchar.key.ENTER):
            cutie.prompt_yes_or_no("foo")
            self.assertEqual(mock_print.call_args_list[-5:], expected_calls)

    @mock.patch("cutie.print")
    def test_write_keypress_to_terminal(self, mock_print):
        expected_calls = [
            (tuple(),),
            print_call("Yes"),
            print_call("No", "selected"),
            (
                ("\x1b[3A\r\x1b[Kfoo (Y/N) ",),
                {"end": "", "flush": True},
            ),
            (tuple(),),
            print_call("Yes"),
            print_call("No"),
            (
                ("\x1b[3A\r\x1b[Kfoo (Y/N) f",),
                {"end": "", "flush": True},
            ),
            (tuple(),),
            print_call("Yes"),
            print_call("No"),
            (
                ("\x1b[3A\r\x1b[Kfoo (Y/N) fo",),
                {"end": "", "flush": True},
            ),
            (tuple(),),
            print_call("Yes"),
            print_call("No"),
            (
                ("\x1b[3A\r\x1b[Kfoo (Y/N) foo",),
                {"end": "", "flush": True},
            ),
        ]
        with InputContext("f", "o", "o", readchar.key.CTRL_C):
            with self.assertRaises(KeyboardInterrupt):
                cutie.prompt_yes_or_no("foo")
            self.assertEqual(mock_print.call_args_list, expected_calls)

    @mock.patch("cutie.print")
    def test_write_keypress_to_terminal_resume_selection(self, mock_print):
        expected_calls = [
            (tuple(),),
            print_call("Yes", "selected"),
            print_call("No"),
            (
                ("\x1b[3A\r\x1b[Kfoo (Y/N) Yes",),
                {"end": "", "flush": True},
            ),
            (("\x1b[K\n\x1b[K\n\x1b[K\n\x1b[3A",),),
        ]
        with InputContext("f", readchar.key.DOWN, readchar.key.ENTER):
            self.assertTrue(cutie.prompt_yes_or_no("foo"))
            self.assertEqual(mock_print.call_args_list[-5:], expected_calls)

    @mock.patch("cutie.print")
    def test_evaluate_written_input_yes_ignorecase(self, mock_print):
        expected_calls = [
            (tuple(),),
            print_call("Yes", "selected"),
            print_call("No"),
            (
                ("\x1b[3A\r\x1b[Kfoo (Y/N) yes",),
                {"end": "", "flush": True},
            ),
            (("\x1b[K\n\x1b[K\n\x1b[K\n\x1b[3A",),),
        ]
        with InputContext("y", "e", "s", readchar.key.ENTER):
            self.assertTrue(cutie.prompt_yes_or_no("foo"))
            self.assertEqual(mock_print.call_args_list[-5:], expected_calls)

    @mock.patch("cutie.print")
    def test_evaluate_written_input_yes_case_sensitive(self, mock_print):
        expected_calls = (
            ("\x1b[3A\r\x1b[Kfoo (Y/N) yes",),
            {"end": "", "flush": True},
        )

        with InputContext("y", "e", "s", readchar.key.CTRL_C):
            res = None
            with self.assertRaises(KeyboardInterrupt):
                res = cutie.prompt_yes_or_no("foo", has_to_match_case=True)
            self.assertIsNone(res)
            self.assertEqual(mock_print.call_args_list[-1], expected_calls)

    @mock.patch("cutie.print")
    def test_evaluate_written_input_no_ignorecase(self, mock_print):
        expected_calls = [
            (tuple(),),
            print_call("Yes"),
            print_call("No", "selected"),
            (
                ("\x1b[3A\r\x1b[Kfoo (Y/N) no",),
                {"end": "", "flush": True},
            ),
            (("\x1b[K\n\x1b[K\n\x1b[K\n\x1b[3A",),),
        ]
        with InputContext("n", "o", readchar.key.ENTER):
            self.assertFalse(cutie.prompt_yes_or_no("foo"))
            self.assertEqual(mock_print.call_args_list[-5:], expected_calls)

    @mock.patch("cutie.print")
    def test_evaluate_written_input_no_case_sensitive(self, mock_print):
        expected_calls = (
            ("\x1b[3A\r\x1b[Kfoo (Y/N) no",),
            {"end": "", "flush": True},
        )

        with InputContext("n", "o", readchar.key.CTRL_C):
            res = None
            with self.assertRaises(KeyboardInterrupt):
                res = cutie.prompt_yes_or_no("foo", has_to_match_case=True)
            self.assertIsNone(res)
            self.assertEqual(mock_print.call_args_list[-1], expected_calls)
