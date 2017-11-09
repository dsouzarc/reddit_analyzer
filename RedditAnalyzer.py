"""RedditAnalyzer.py: Main class; Responsible for actually analyzing all subreddits"""

import json
import random

from RedditClientConfig import RedditClientConfig

import praw


#For analyzing a subreddit
class SubredditAnalyzer(object):
    """Analyzes a specific subreddit"""

    reddit_client = None
    subreddit_name = None

    def __init__(self, reddit_client, subreddit_name):
        """Initializer

        Args:
            reddit_client (praw.Reddit): the client to analyze this subreddit
            subreddit_name (str): name of the subreddit
        """

        self.reddit_client = reddit_client
        self.subreddit_name = subreddit_name


    def get_subreddit_counts(self):
        """Gets the subreddits and returns information to be analyzed"""

        subreddit = self.reddit_client.subreddit(self.subreddit_name)
        print("For: %s\t%s" % (self.subreddit_name, subreddit.subscribers))





#Our main analyzer
class RedditAnalyzer(object):
    """Main analyzer"""

    reddit_clients = None
    subreddit_analyzers = None
    configuration = None

    def __init__(self, configuration_file="configuration.json"):

        self.reddit_clients = dict()
        self.subreddit_analyzers = dict()
        self.configuration = json.load(open(configuration_file, 'r'))

        reddit_users = self.configuration.get("reddit_users", list())
        for reddit_user_dict in reddit_users:
            reddit_client = RedditClientConfig(reddit_user_dict)
            self.reddit_clients[reddit_client.username] = reddit_client

        subreddit_names = self.configuration.get("subreddit_names", list())
        for subreddit_name in subreddit_names:
            reddit_client = random.choice(self.reddit_clients.values()).get_client()
            subreddit_analyzer = SubredditAnalyzer(reddit_client, subreddit_name)
            self.subreddit_analyzers[subreddit_name] = subreddit_analyzer


    def users_online(self):
        for subreddit, analyzer in self.subreddit_analyzers.iteritems():
            analyzer.get_subreddit_counts()


reddit_analyzer = RedditAnalyzer()
reddit_analyzer.users_online()
