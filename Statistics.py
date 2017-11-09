"""Statistics.py Contains various objects used for calculating statistics"""

from abc import ABCMeta
from abc import abstractmethod
from bson import json_util
from datetime import datetime

import json


#Abstract Base class - All objects must extend and implement
class Statistic(metaclass=ABCMeta):
    """Base Statistics class - the base representation"""

    subreddit = None
    timestamp = None

    def __init__(self, subreddit, timestamp=datetime.utcnow()):
        """Default constructor

        Args:
            subreddit (str): name of the subreddit
            timestamp (datetime): timestamp for the statistic
        """
            
        self.subreddit = subreddit
        self.timestamp = timestamp


    @abstractmethod
    def storage_dict(self):
        """Return a JSON dict representation of the object that can be stored in MongoDB

        Return:
            (dict) representation of object that can be inserted into MongoDB
        """
        pass


#Quick snapchat of a subreddit's Statistics
class SubredditStatistic(Statistic):
    """Represents information about a subreddit"""

    subscribers_online = None
    total_subscribers = None
    online_ratio = None

    def __init__(self, subreddit, timestamp, subscribers_online, total_subscribers):
        """Constructor

        Args:
            subscribers_online (int): number of subscribers online right now
            total_subscribers (int): total number of subscribers, including online
        """

        super(SubredditStatistic, self).__init__()
        self.subscribers_online = subscribers_online
        self.total_subscribers = total_subscribers
        self.online_ratio = float(subscribers_online) / total_subscribers


    def storage_dict(self):
        """See Statistics Abstract Base Class"""

        return vars(self)

        



