# -*- coding: utf-8 -*-
"""
reddit_slack_bot.slack
~~~~~~~~~~~~
This module handles slack interactions
:copyright: (c) 2018 by Henry Gan.
"""

import configparser
import time
import re
import structlog
from slackclient import SlackClient

# constants
CONFIG = configparser.ConfigParser()
CONFIG.read('config/CONFIG')
SLACKBOT = CONFIG['slackbot']
LOG = structlog.get_logger()
TAG = "slack"
RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

# instantiate Slack client
slack_client = SlackClient(SLACKBOT['bot_user_oauth_access_token'])
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None


def parse_bot_commands(slack_events):
    """ Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.

    Arguments:
        slack_events {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None


def parse_direct_mention(message_text):
    """ Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None

    Arguments:
        message_text {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None,
                                                                         None)


def handle_command(command, channel):
    """ Executes bot command if the command is known
    
    Arguments:
        command {[type]} -- [description]
        channel {[type]} -- [description]
    """

    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(
        EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage", channel=channel, text=response or default_response)


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        LOG.msg(TAG, "Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        LOG.msg(TAG, "Connection failed. Exception traceback printed above.")
