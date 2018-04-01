# coding=utf-8
import logging

from slacker import Slacker
from slacksocket import SlackSocket

from config import Config, ConfigKeys


class SlackMessageBroker(object):

    def send_reaction(self, slack_event_to_react_to):
        try :
            slack = Slacker(self.token)
            slack.reactions.add(name="robot_face",
                                channel=slack_event_to_react_to["channel_id"],
                                timestamp=slack_event_to_react_to["ts"])
        except Exception:
            logging.exception("Error sending reaction to: " + str(slack_event_to_react_to))

    def send_message(self, message_text, channel):
        if self.debug:
            message_text = "[DEBUG] " + message_text
        try :
            with SlackSocket(self.token) as s:
                msg = s.send_msg(message_text, channel)
                logging.info(msg.sent)
        except Exception:
            logging.exception("Error sending message response to: " + channel)

    def send_dm(self, message_text, user_slack_id):
        if self.debug:
            message_text = "[DEBUG] " + message_text
        try:
            slack = Slacker(self.token)
            im = slack.im.open(user_slack_id).body
            if im["ok"]:
                channel_id = im["channel"]["id"]
                slack.chat.post_message(channel_id, text=message_text)

            else:
                raise Exception("Failed to open a DM to send response.")

        except Exception:
            logging.exception("Error sending DM response to: " + str(user_slack_id))

    def __init__(self, debug=False):
        self.debug = debug
        config = Config()
        self.token = config.get_config_value(ConfigKeys.slack_bot_token)