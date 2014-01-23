django-antispam
===============

Antispam is a django middleware for anti spam.

It depends on [django-redis](<https://github.com/niwibe/django-redis>).

Content
-------

It contains 4 parts:

* __White ip list__
    
    redis key: ``antispam:white_ip``

    demo: ``sadd antispam:white_ip 202.205.10.93``  

* __White http user agent list__

    redis key: ``antispam:white_ua``

    demo: ``sadd antispam:white_ua 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'``  

* __Black ip list__

    redis key: ``antispam:black_ip``

    demo: ``sadd antispam:black_ip 202.205.10.93``  

* __Black http user agent list__

    redis key: ``antispam:black_ip``

    demo: ``sadd antispam:black_ua 'LG/U8120/v1.0'``  


White list has the first priority. That means if an ip is both in white list and ban in black list. 
The black list won't work.

Quick Start
-----------

* __Install__

    ```shell
    pip install git+https://github.com/yijingping/django-antispam#egg=django_antispam
    ```

* __Add this lines in the end of  your setting__

    ```python
    # enable anti spam, default is True
    ANTI_SPAM = True
    if ANTI_SPAM:
        # installed
        INSTALLED_APPS += ( 'antispam',)
        MIDDLEWARE_CLASSES += ( 'antispam.middleware.AntiSpamFilterMiddleware',)
        # use redis backend cache, set cache key here 
        ANTI_SPAM_CACHE_REDIS_KEY = 'redis'
        # flush ip,ua from redis, every 10 minutes
        ANTI_SPAM_DELTA_FLUSH_TIME = 60 * 10 
        # invoke this view function when it's a spam 
        ANTI_SPAM_SPAM_VIEW = 'django.views.defaults.page_not_found'
    ```

* __Add white/black list list in your redis__
   
    ```shell 
    $ redis-cli -h 192.168.10.85 -p 6379
    > sadd sadd antispam:black_ua 'LG/U8120/v1.0'
    > sadd sadd antispam:black_ip '112.64.16.8' 
    ```

* __Start your project, and check__

* __Notice when change white/black list__
    
   Antispam flush white/black list every ``ANTI_SPAM_DELTA_FLUSH_TIME`` seconds which is set in your settings.py.

   So, if your change dose not work, check the time first. 
