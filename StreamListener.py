import logging
import tweepy
from archive import archive_tweet
from constants import *


class StreamListener(tweepy.StreamListener):
    def __init__(self, q):
        super(StreamListener, self).__init__()
        self.q = q

    def on_status(self, status):
        self.q.put(status)

    def on_error(self, status_code):
        logger = logging.getLogger("error")
        logger.error("Tweepy error {}".format(status_code))
