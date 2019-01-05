# -*- coding: utf-8 -*-
"""
reddit_slack_bot.reddit
~~~~~~~~~~~~
This module handles reddit auth and API commands
:copyright: (c) 2018 by Henry Gan.
"""
import configparser
import praw

from config.rules import ban_reasons as BAN_REASONS
CONFIG = configparser.ConfigParser()
CONFIG.read('config/CONFIG')

AUTH = CONFIG['auth']
REDDIT_CONFIG = CONFIG['reddit']


class SubredditMod:
    """Reddit class that executes moderation actions"""

    def __init__(self,
                 subreddit=REDDIT_CONFIG['subreddit'],
                 username=AUTH['username'],
                 password=AUTH['password'],
                 client_id=AUTH['client_id'],
                 client_secret=AUTH['client_secret'],
                 user_agent=AUTH['user_agent']):
        """Initializes the SubredditMod class. Creates the reddit and subreddit
        variables for use.

        **Currently does not support Two-Factor Auth.**

        If not known, the information can be found and created here
        https://www.reddit.com/prefs/apps/

        Arguments:
            subreddit {str} -- The subreddit name to use the mod actions on.
                Defaults to CONFIG file value in reddit.subreddit
            username {str} -- The username of the Reddit account used to
                register the script application.
                Defaults to CONFIG file value in auth.username
            password {str} -- The password for the Reddit account used to
                register the script application.
                Defaults to CONFIG file value in auth.password
            client_id {str} -- The client ID is the 14 character string
                listed just under “personal use script” for the desired
                developed application
                Defaults to CONFIG file value in auth.client_id
            client_secret {str} -- The client secret is the 27 character
                string listed adjacent to secret for the application.
                Defaults to CONFIG file value in auth.client_secret
            user_agent {str} -- UserAgent of client. Should be unique and
                descriptive, including the target platform, a unique
                application identifier, a version string, and your username
                as contact information
                Defaults to CONFIG file value in auth.user_agent
        """
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            password=password,
            user_agent=user_agent,
            username=username)
        self.subreddit = self.reddit.subreddit(subreddit)

    def ban(self, user, reason, **kwargs):
        """Ban user from subreddit.

        Reason must be a key available in ban_reasons (found in rules.py)

        kwargs must be one or more of these:
            ban_message {str}: The ban message which is sent to the user
            duration {int}: The length of ban, in days. Blank for perm
            note {str}: A note about the ban, not sent to the user

        Arguments:
            user {str} -- Username
            reason {str} -- Ban reason. Use rule number
        """

        self.subreddit.banned.add(user, reason=BAN_REASONS[reason], **kwargs)

    def rules(self):
        """Return rules for the subreddit.

        Returns:
            str -- String of the subreddit rules
        """

        return self.subreddit.rules()

    def traffic(self):
        """Return a dictionary of the subreddit’s traffic statistics.

        Returns:
            dict -- Dict of subreddit traffic statistics
        """

        return self.subreddit.traffic()
