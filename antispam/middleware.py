'''
antispam middleware 
'''

from __future__ import unicode_literals
import time
from django.conf import settings
from redis_cache import get_redis_connection
from django.core.urlresolvers import get_callable

SPAM_VIEW = get_callable(settings.ANTI_SPAM_SPAM_VIEW)
KEY_WHITE_IP = 'antispam:white_ip'
KEY_WHITE_UA = 'antispam:white_ua'
KEY_BLACK_IP = 'antispam:black_ip'
KEY_BLACK_UA = 'antispam:black_ua'
CACHE_WHITE_IP= set()
CACHE_WHITE_UA= set()
CACHE_BLACK_IP= set()
CACHE_BLACK_UA= set()
LAST_FLUSH_TIME = time.time() - settings.ANTI_SPAM_DELTA_FLUSH_TIME

def flush():
    global KEY_WHITE_IP, KEY_WHITE_UA, KEY_BLACK_IP, KEY_BLACK_UA 
    global CACHE_WHITE_IP, CACHE_WHITE_UA, CACHE_BLACK_IP, CACHE_BLACK_UA
    conn = get_redis_connection(settings.ANTI_SPAM_CACHE_REDIS_KEY)
    CACHE_WHITE_IP = conn.smembers(KEY_WHITE_IP)
    CACHE_WHITE_UA = conn.smembers(KEY_WHITE_UA)
    CACHE_BLACK_IP = conn.smembers(KEY_BLACK_IP)
    CACHE_BLACK_UA = conn.smembers(KEY_BLACK_UA)


def get_ip(request):
    if request.META.get('HTTP_CLIENT_IP'):
        return request.META.get('HTTP_CLIENT_IP')
    elif request.META.get('HTTP_X_FORWARDED_FOR'):
        # maybe many proxy ips
        ips = request.META.get('HTTP_X_FORWARDED_FOR')
        return ips.split(',')[0].split()[0]
    else:
        return request.META.get('REMOTE_ADDR', '')

def get_user_agent(request):
    return request.META.get('HTTP_USER_AGENT','') 


class AntiSpamFilterMiddleware(object):
    def process_request(self, request):
        global LAST_FLUSH_TIME
        global CACHE_WHITE_IP, CACHE_WHITE_UA, CACHE_BLACK_IP, CACHE_BLACK_UA
        # check enable
        if not settings.ANTI_SPAM:
            return None

        # flush white list cache, black list cache
        now = time.time()
        if now - LAST_FLUSH_TIME > settings.ANTI_SPAM_DELTA_FLUSH_TIME:
            LAST_FLUSH_TIME = now
            flush()

        ip = get_ip(request)
        ua = get_user_agent(request) 
        # filter white list
        if ip in CACHE_WHITE_IP or ua in CACHE_WHITE_UA: 
            return None

        # filter black list 
        if ip in CACHE_BLACK_IP or ua in CACHE_BLACK_UA: 
            return SPAM_VIEW(request)

        # neigher in white list, nor in balck list 
        return None


class AntiSpamDetectMiddleware(object):
    pass
