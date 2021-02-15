import logging
import tweepy


class StreamListener(tweepy.StreamListener):
    def __init__(self, q):
        super(StreamListener, self).__init__()
        self.q = q

    def on_status(self, status):
        self.q.put(status)

    def on_error(self, status_code):
        logger = logging.getLogger("error")
        error_str = "Tweepy error {}".format(status_code)
        logger.error(error_str)
