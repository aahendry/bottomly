# coding=utf-8
import unittest
from unittest.mock import patch
from commands import GoogleSearchCommand
from config import Config
from slack_channel import GoogleEventHandler

test_prefix = "_"
valid_event = {"text": test_prefix + "g a valid google command"}
invalid_event = {"text": "this is missing a valid command prefix"}
google_response = {"title": "response title", "link": "response_link"}

class TestGoogleEventHandler(unittest.TestCase):

    @patch.object(Config, "get_config_value")
    @patch.object(Config, "get_prefix", return_value=test_prefix)
    def test_handles_correct_event(self, prefix_method, config_method):
        handler = GoogleEventHandler()
        can_handle = handler.can_handle(valid_event)
        self.assertTrue(can_handle)

    @patch.object(Config, "get_config_value")
    @patch.object(Config, "get_prefix", return_value=test_prefix)
    def test_does_not_handle_different_event(self, prefix_method, config_method):
        handler = GoogleEventHandler()
        can_handle = handler.can_handle(invalid_event)
        self.assertFalse(can_handle)

    @patch.object(Config, "get_prefix", return_value=test_prefix)
    @patch.object(Config, "get_config_value")
    @patch.object(GoogleEventHandler, "_send_response")
    @patch.object(GoogleSearchCommand, "execute", return_value = google_response)
    def test_command_execute_is_called(self, execute_method, response_method, config_method, prefix_method):
        handler = GoogleEventHandler()
        handler.handle(valid_event)
        execute_method.assert_called_with(valid_event["text"][3:])

    @patch.object(Config, "get_prefix", return_value=test_prefix)
    @patch.object(Config, "get_config_value")
    @patch.object(GoogleSearchCommand, "execute", return_value=google_response)
    @patch.object(GoogleEventHandler, "_send_response")
    def test_command_result_is_correctly_built(self, response_method, execute_method, config_method, prefix_method):
        handler = GoogleEventHandler()
        handler.handle(valid_event)
        response_method.assert_called_with("response title response_link", valid_event)

    if __name__ == '__main__':
        unittest.main()