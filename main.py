import logging
import logging.handlers
import queue
import tweepy
from archive import archive_worker
from constants import *
from secrets import *
from StreamListener import StreamListener
from threading import Thread


def configure_logs():
    tweet_logger = logging.getLogger("tweets")
    tweet_logger.setLevel(logging.INFO)
    fh = logging.handlers.RotatingFileHandler(
        LOGFILE_NAME, maxBytes=500000000, backupCount=100, encoding="utf-8"
    )
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z"
    )
    fh.setFormatter(formatter)
    tweet_logger.addHandler(fh)

    error_logger = logging.getLogger("error")
    error_logger.setLevel(logging.ERROR)
    error_fh = logging.handlers.RotatingFileHandler(
        "error.log", maxBytes=500000000, backupCount=5, encoding="utf-8"
    )
    error_fh.setLevel(logging.ERROR)
    error_fh.setFormatter(formatter)
    error_logger.addHandler(error_fh)


def run():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    configure_logs()
    _sentinel = object()
    q = queue.Queue()
    listener = StreamListener(q)
    stream = tweepy.Stream(auth=api.auth, listener=listener)

    try:
        print("Stream starting.")
        thread = Thread(target=archive_worker, args=(q, _sentinel))
        thread.daemon = True
        thread.start()
        q.join()
        stream.filter(follow=[TWITTER_USER_ID_STR])
    except KeyboardInterrupt:
        q.put(_sentinel)
        stream.disconnect()
        print("Stream disconnected.")


if __name__ == "__main__":
    run()
