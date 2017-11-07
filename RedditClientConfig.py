"""RedditClientConfig.py Represents the config needed to initialize a Reddit Praw object"""

import json
import random

import praw

class RedditClientConfig(object):

    #Static variables
    user_agents_file_name = "user_agents.txt"
    user_agents = None

    #Instance variables
    username = None
    password = None
    client_id = None
    client_secret = None
    user_agent = None


    def __init__(self, config_dict, user_agent=None, random_user_agent=True):
        """Initializer

        Args:
            config_dict (dict): reddit client configuration
        """

        self.username = config_dict.get("username", "")
        self.password = config_dict.get("password", "")
        self.client_id = config_dict.get("client_id", "")
        self.client_secret = config_dict.get("client_secret", "")
        self.user_agent = config_dict.get("user_agent", user_agent)

        if self.user_agent is None or random_user_agent:

            #Update the static user_agents with all the user agents
            if RedditClientConfig.user_agents is None:
                RedditClientConfig.user_agents = list()
                user_agents_file = open(RedditClientConfig.user_agents_file_name, 'r')

                for user_agent in user_agents_file:
                    RedditClientConfig.user_agents.append(user_agent)

            #Choose a random user agent
            rand_index = random.randrange(0, len(RedditClientConfig.user_agents))
            self.user_agent = RedditClientConfig.user_agents[rand_index]
            del RedditClientConfig.user_agents[rand_index]

    def get_client(self):
        """Creates a praw.Reddit client and returns it

        Returns:
            praw.Reddit: initialized client
        """

        client = praw.Reddit(username=self.username,
                                password=self.password,
                                client_id=self.client_id,
                                client_secret=self.client_secret,
                                user_agent=self.user_agent)

        return client
