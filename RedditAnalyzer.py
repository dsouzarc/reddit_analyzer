"""RedditAnalyzer.py: Main class; Responsible for actually analyzing all subreddits"""

#Standard libraries
from datetime import datetime

import json
import random
import time

#Project-specific modules
from RedditClientConfig import RedditClientConfig
from Statistics import Statistic
from Statistics import SubredditStatistic

#3rd party libraries
from bson import json_util
from pymongo import MongoClient

import praw
import pymongo


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

        try:
            subreddit = self.reddit_client.subreddit(self.subreddit_name)
        except Exception as e:
            print("Error getting subreddit: %s " % e)
        else:
            subscribers_online = (subreddit.active_user_count + subreddit.accounts_active) / 2
            total_subscribers = subreddit.subscribers

            statistics = SubredditStatistic(subreddit=self.subreddit_name,
                                            timestamp=datetime.utcnow(),
                                            subscribers_online=subscribers_online,
                                            total_subscribers=total_subscribers)
        return statistics


class RedditAnalyzer(object):
    """Main analyzer"""

    reddit_clients = None
    subreddit_analyzers = None
    configuration = None

    database = None
    subreddit_stats = None

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
        self.subreddit_stats = self.database["subreddit_stats"]


    def users_online(self):
        for subreddit, analyzer in self.subreddit_analyzers.iteritems():
            print("Trying: %s" % subreddit)
            statistics = analyzer.subreddit_statistics()
            print("Got: %s" % statistics)

            try:
                inserted_result = self.subreddit_stats.insert_one(statistics.storage_dict())
            except Exception as e:
                print("Error inserting subreddit data: % " % e)
            else:
                print(statistics.storage_dict())
                print(inserted_result)
            finally:
                time.sleep(1)


if __name__ == "__main__":
    """Main method"""

    reddit_analyzer = RedditAnalyzer()

    while True:
        start = time.time()
        try:
            reddit_analyzer.users_online()
        except Exception as e:
            print("Error calculating: %s" % e)
        finally:
            end = time.time()
            print("Finished subreddits in %s - sleeping now" % (end - start))
            time.sleep(5 * 60 - (end - start))
