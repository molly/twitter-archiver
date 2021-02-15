import logging
import requests
import threading
from constants import *
from requests.adapters import HTTPAdapter


def archive_tweet(tweet_url):
    session = requests.Session()
    session.headers.update(HEADERS)
    session.mount(ARCHIVE_URL, adapter=HTTPAdapter(max_retries=3))
    try:
        r = session.get(
            ARCHIVE_URL + tweet_url,
            headers=HEADERS,
            data={"url": tweet_url},
            timeout=60,
        )
        r.raise_for_status()
        return r.url
    except requests.exceptions.HTTPError as e:
        logger = logging.getLogger("error")
        error_str = "HTTP {} error while trying to archive {}.".format(
            e.response.status_code, tweet_url
        )
        logger.exception(error_str)
        return None
    except requests.exceptions.Timeout as e:
        logger = logging.getLogger("error")
        error_str = "Request timed out while trying to archive {}.".format(tweet_url)
        logger.exception(error_str)
        return None
    except requests.exceptions.ConnectionError as e:
        logger = logging.getLogger("error")
        error_str = "Connection error while trying to archive {}.".format(tweet_url)
        logger.exception(error_str)
        return None
    except requests.exceptions.RequestException as e:
        logger = logging.getLogger("error")
        error_str = "Other exception while trying to archive {}.".format(tweet_url)
        logger.exception(error_str)
        return None


def archive_worker(q, _sentinel):
    while True:
        status = q.get()
        if status is _sentinel:
            q.task_done
            break
        elif status.author.id == TWITTER_USER_ID:
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
        q.task_done()
