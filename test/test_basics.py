# -*- coding: utf-8 -*-
from csirtg_urlsml import predict
from faker import Faker
from random import sample
fake = Faker()
from pprint import pprint
from time import time
import os

URLS = [
    'http://58.147.128.10:81/val/1.html',
    'http://192.168.1.1/1.html',
    'http://www41.xzmnt.com',
    'http://get.ahoybest.com/n/3.6.16/12205897/microsoft lync server 2010.exe',
    'http://webmail.epuc.com.br:32000/mail/settings.html',
    'http://www.@sokoyetu.co.ke/aol5/a000l.html',
    'https://example.com:443/1.html',
    'http://test1.test2.example.com',
    'http://xz.job391.com/down/ï¿½ï¿½ï¿½ï¿½à¿ªï¿½ï¿½@89_1_60',
    'http://refreshdharan.com/bg/excel2/index.php?userid={dong.keonkwonfinancialconsultd@yahoo.com}',
    'http://https.www.paypal.blahblahblahblah.web.cgi.bin.blahblah.blahblahblahblah.blahblahblah-blah-blah-blah.com/signin/',
    'http://ppleid.apple.com.account.manage.wets.myapleid.woa.wa.directt.myappleid.woa.25napplic2faccount.25napplic2faccountmyappleid.woa9limgdpx25napplic2faccountmya4343.25woa9limgdpx25napplic2faccountmya4343.25nap.bhsfser.com/c13cc8f750e0e241e2d23f5e2ded1706/index/src/index/index.php'
]

THRESHOLD = 0.92
SAMPLE = int(os.getenv('CSIRTG_URLSML_TEST_SAMPLE', 1000))


def _stats(u, inverse=False):
    n = 0
    positives = 0
    t1 = time()
    for p in u:
        p = predict(p)
        if (inverse and p == 0) or p == 1:
            positives += 1
        n += 1

    t2 = time()
    total = t2 - t1
    per_sec = SAMPLE / total
    print("seconds: %.2f" % total)
    print("rate: %.2f" % per_sec)

    n = (float(positives) / n)
    print(n)
    return n


def test_urls_basic():
    assert _stats(URLS) >= .8


def test_urls_random():
    s = []
    for d in range(0, SAMPLE):
        s.append(str(fake.uri()))

    n = _stats(s)
    assert n > .9


def test_urls_blacklist():
    u = []
    with open('data/blacklist.txt') as FILE:
        for l in FILE.readlines():
            l = l.rstrip("\n")
            u.append(l)

    u = sample(u, SAMPLE)

    n = _stats(u)
    assert n > THRESHOLD


def test_urls_whitelist():
    u = []
    with open('data/whitelist.txt') as FILE:
        for l in FILE.readlines():
            l = l.rstrip("\n")
            u.append(l)

    urls = sample(u, SAMPLE)
    n = _stats(urls, inverse=True)
    assert n > THRESHOLD
