import http
import logging
import tweepy
from archive import archive_worker
from urllib3.exceptions import ProtocolError


class StreamListener(tweepy.StreamListener):
    def __init__(self, executor):
        super(StreamListener, self).__init__()
        self.executor = executor

    def on_status(self, status):
        self.executor.submit(archive_worker, status)

    def on_error(self, status_code):
        logger = logging.getLogger("error")
        error_str = "Tweepy error {}".format(status_code)
        logger.error(error_str)

    def on_exception(self, exception):
        if isinstance(exception, http.client.IncompleteRead) or isinstance(
            exception, ProtocolError
        ):
            return True
        return False
