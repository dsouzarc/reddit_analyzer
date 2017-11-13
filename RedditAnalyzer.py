"""RedditAnalyzer.py: Main class; Responsible for actually analyzing all subreddits"""

#Standard libraries
from datetime import datetime

import json
import random

#Project-specific modules
from RedditClientConfig import RedditClientConfig
from Statistics import Statistic
from Statistics import SubredditStatistic

#3rd party libraries
from bson import json_util
from pymongo import MongoClient

import praw
import pymongo


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





    def subreddit_statistics(self):
        """Calculates the Statistics for this particular subreddit

        Return:
            (SubredditStatistic): object holding the current statistics for this subreddit
        """

        subreddit = self.reddit_client.subreddit(self.subreddit_name)
        subscribers_online = (subreddit.active_user_count + subreddit.accounts_active) / 2
        total_subscribers = subreddit.subscribers

        statistics = SubredditStatistic(subreddit=self.subreddit_name,
                                        timestamp=datetime.utcnow(),
                                        subscribers_online=subscribers_online,
                                        total_subscribers=total_subscribers)
        return statistics


#Our main analyzer
class RedditAnalyzer(object):
    """Main analyzer"""

    reddit_clients = None
    subreddit_analyzers = None
    configuration = None

    database = None
    subreddit_collection = None

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

        database_configuration = self.configuration.get("database_configuration")
        mongo_client_host = ("mongodb://{username}:{password}@{ip_address}:{port}/"
                                .format(username=database_configuration["username"],
                                            password=database_configuration["password"],
                                            ip_address=database_configuration["ip_address"],
                                            port=database_configuration["port"]))
        database_client = MongoClient(mongo_client_host)
        self.database = database_client["Reddit"]
        self.subreddit_collection = self.database["subreddit"]


    def users_online(self):
        for subreddit, analyzer in self.subreddit_analyzers.iteritems():
            statistics = analyzer.subreddit_statistics()
            print(statistics.storage_dict())


reddit_analyzer = RedditAnalyzer()
reddit_analyzer.users_online()

