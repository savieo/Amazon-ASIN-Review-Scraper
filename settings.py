from useragent import get_ua
from redis import StrictRedis
import random
from random import choice
redis = StrictRedis('172.16.253.235',db=5)
ualist = redis.smembers("desktop_ua")

def get_ua():
    return choice(list(ualist))
# REDIS_URL = 'localhost'
# REDIS_PORT = 6379
# REDIS_DB = 1

# TIME_ZONE = 'UTC'
# RESUME = False
MAX_RETRY = 30
# UNIQUE_CHECK = True
THREADS = 25

# AUTOTHROTTLE = False
# TIMEOUT = 5
MIN_DELAY = 2
MAX_DELAY = 30
# REQUEST_PROCESSOR = 'dragline.http:RequestProcessor'

DEFAULT_REQUEST_ARGS = {
    # 'allow_redirects': True,
    # 'auth': None,
    # 'cert': None,
    # 'cookies': None,
    # 'data': None,
    # 'files': None,
    'headers':{
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding":"gzip, deflate, sdch, br",
                "Accept-Language":"en-GB,en-US;q=0.8,en;q=0.6",
                "Cache-Control":"max-age=0",
                "Connection":"keep-alive",
                "Host":"www.amazon.com",
                "Upgrade-Insecure-Requests":"1",
                "X-Proxy-Country":"US",
                "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
                },
    # 'json': None,
    # 'method': None,
    # 'params': None,
    # 'proxies': lambda : random.choice([{"https":"http://scrapehero:LQMw54Ken00mP0Cj@us-ny.proxymesh.com:31280","http":"http://scrapehero:LQMw54Ken00mP0Cj@us-ny.proxymesh.com:31280"},
    #                             {"https":"http://scrapehero:LQMw54Ken00mP0Cj@us-ca.proxymesh.com:31280","http":"http://scrapehero:LQMw54Ken00mP0Cj@us-ca.proxymesh.com:31280"}
    #                             ]),
    # 'stream': False,
    # 'timeout': None,
    # 'verify': False
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
        'dragline': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
        '1796_amazon': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

try:
    from local_settings import *
except:
    pass
