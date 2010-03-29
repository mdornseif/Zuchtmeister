#!/usr/bin/env python
# encoding: utf-8
"""
twitter.py

Created by Maximillian Dornseif on 2010-03-28.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

# see http://www.b-list.org/weblog/2007/sep/22/standalone-django-scripts/
#from django.core.management import setup_environ
#import settings
#setup_environ(settings)

#Yahoo:
# API Key (OAuth consumer key)
# dj0yJmk9NVo1QnJhYW1EQXJ3JmQ9WVdrOVowbGhZVlJFTkc4bWNHbzlNVGt3TURrME5qazJNZy0tJnM9Y29uc3VtZXJzZWNyZXQmeD05Zg--
# Shared Secret
# f8e7987b1eec2e687580978482504d32ca5a5ae0
# Application ID
# gIaaTD4o
# Application Domain
# asksheila.org

import tweepy
from taskmaster import models
from django.conf import settings


def _init_api():
    """Get an tweepy.API object with authentication beeing already set up."""
    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN_KEY, settings.TWITTER_ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)


def connetion_ok(account):
    """Verifies follower relationship and sends greeting message if apropriate."""
    if account.twitter_user:
        if account.twitter_user != account.verified_twitter_user:
            if account.verified_twitter_user:
                account.verified_twitter_user = ''
                account.save()
            api = _init_api()
            user = api.get_user(account.twitter_user)
            if not user.following:
                user.follow()
            try:
                api.send_direct_message(user=account.twitter_user,
                                        text="Hi, this is Sheila. Looking forward to work with you via Twitter! More at http://asksheila.org/main")
            except tweepy.error.TweepError as inst:
                if str(inst) == 'You cannot send messages to users who are not following you.':
                    if account.verified_twitter_user:
                        account.verified_twitter_user = ''
                        account.save()
                    return False
                else:
                    raise
            account.verified_twitter_user = account.twitter_user
            account.save()
    return True


def maintenance():
    """Periodical consistency checks."""
    api = _init_api()
    all_followers = set()
    # follow everybody who follows us and has an Account
    for user in tweepy.Cursor(api.followers).items():
        all_followers.add(user.screen_name)
        if models.Account.objects.filter(twitter_user=user.screen_name).count():
            # follow back
            if not user.following:
                user.follow()


def handle_direct_messages():
    api = _init_api()
    for dm in api.direct_messages():
        # The following following code does not work as expected
        # if not dm.sender.following:
        #     # shout never happen, but better safe than sorry
        #     dm.sender.follow()
        accounts = list(models.Account.objects.filter(twitter_user=dm.sender.screen_name))
        if len(accounts) < 1:
            api.send_direct_message(user=dm.sender.screen_name,
                                    text="Hi, Sheila here. I'm terribly sorry, but I forgot where we met and I don't have you in my files. Could you log in at http://asksheila.org/?")
        else:
            account = accounts[0]
            # TODO: use objects.get_or_create()
            if models.Op.objects.filter(account=account, tweet_id=dm.id).count() < 1:
                models.Op.objects.create(account=account, task=dm.text, tweet_id=dm.id)
            else:
                print 'duplicate message', vars(dm)
                pass
        api.destroy_direct_message(dm.id)

