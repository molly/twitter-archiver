import logging
import tweepy
from archive import archive_tweet
from constants import *


class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if status.author.id == TWITTER_USER_ID:
            logger = logging.getLogger("tweets")
            if status.user.id == TWITTER_USER_ID:
                # This is an original tweet, so just archive
                url = URL_PREFIX + status.id_str
                archived_url = archive_tweet(url)

                logger.info(
                    "Tweeted: {text}\n"
                    "{url}{archived_url}".format(
                        text=status.text,
                        url=url,
                        archived_url=""
                        if archived_url is None
                        else " (" + archived_url + ")",
                    )
                )
            else:
                # This is a retweet, so archive the tweet that was retweeted and log it
                url = "https://twitter.com/{user}/status/{status_id}".format(
                    user=status.author.screen_name, status_id=status.id_str
                )

                # Archive
                archived_url = archive_tweet(url)

                # Log
                logger.info(
                    "Retweeted @{user}: {text}\n"
                    "{url}{archived_url}".format(
                        user=status.author.screen_name,
                        text=status.text,
                        url=url,
                        archived_url=""
                        if archived_url is None
                        else " (" + archived_url + ")",
                    )
                )

    def on_error(self, status_code):
        logger = logging.getLogger("error")
        logger.error("Tweepy error {}".format(status_code))
