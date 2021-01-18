import logging
import requests

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
        logger.error(
            "HTTP {} error while trying to archive {}.".format(
                e.response.status_code, tweet_url
            ),
            e,
        )
        return None
    except requests.exceptions.Timeout as e:
        logger = logging.getLogger("error")
        logger.error(
            "Request timed out while trying to archive {}.".format(tweet_url), e
        )
    except requests.exceptions.ConnectionError as e:
        logger = logging.getLogger("error")
        logger.error(
            "Connection error while trying to archive {}.".format(tweet_url), e
        )
    except requests.exceptions.RequestException as e:
        logger = logging.getLogger("error")
        logger.error("Other exception while trying to archive {}.".format(tweet_url), e)
    return None
