from argparse import ArgumentParser, RawDescriptionHelpFormatter
import textwrap
import sys
import numpy as np
import re

from csirtg_domainsml.utils import entropy
from csirtg_domainsml.domain import _extract_features as _extract_domain_features

if sys.version_info > (3,):
    from urllib.parse import urlparse
    basestring = (str, bytes)
else:
    from urlparse import urlparse
from pprint import pprint


# http://www.supermind.org/blog/740/average-length-of-a-url-part-2
def _has_high_length(u):
    l = len(u)

    if l < 52:
        return -1

    if l < 76:
        return 0

    return 1


def _is_image(u):
    if re.search(r'\.[jpg|png|gif]$', u):
        return 1
    return -1


def _is_root_url(u):
    if u.count('/') == 2:
        return 1

    return -1


def _high_slashes(u):
    if u.count('/') == 3:
        return -1

    if u.count('/') < 5:
        return 0

    return 1


def _is_edu(u):
    u = urlparse(u)
    if re.search(r'.edu$', u.netloc):
        return 1
    return -1


def _is_wp_content(u):
    if re.search(r'/wp-content/', u):
        return 1

    return -1


def _is_https(u):
    if u.startswith('https://'):
        return 1
    return -1


def _has_high_entropy(u):
    e = entropy(u)

    if e < 3.86:
        return -1

    if e < 4.25:
        return 0

    return 1


def _is_secure(u):
    for e in ['confirm', 'account', 'banking', 'secure', 'ebayisapi', 'webscr', 'login', 'signin', 'bank']:
        if re.search(e, u):
            return 1
    return -1


FEATURES = [
    _has_high_entropy,
    _is_secure,
    _has_high_length,
    _is_root_url,
    _is_image,
    _high_slashes,
    _is_edu,
    _is_wp_content,
    _is_https,
]


def _extract_features(u):
    if isinstance(u, str):
        u = urlparse(u)

    feats = _extract_domain_features(u.netloc)
    for f in FEATURES:
        r = f(u.geturl().rstrip('/'))
        feats.append(r)

    return feats


def predict(u, classifier):
    if isinstance(u, str):
        u = urlparse(u)

    feats = _extract_features(u)
    feats = np.array(feats, dtype=int)
    return classifier.predict(feats)


def main():
    p = ArgumentParser(
        description=textwrap.dedent('''\
                example usage:
                    $ csirtg-urlsml --training data/training.csv -i http://badsite.com/1.html
                '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='csirtg-urlsml'
    )

    p.add_argument('-d', '--debug', dest='debug', action="store_true")
    p.add_argument('--good', action="store_true", default=False)

    args = p.parse_args()

    for l in sys.stdin:
        l = l.rstrip()
        l = urlparse(l)
        path = l.path
        if path == '/':
            continue

        feats = []
        for f in _extract_features(l):
            feats.append(f)

        if args.good:
            feats.append(0)
        else:
            feats.append(1)

        feats = [str(f) for f in feats]
        out = ','.join(feats)
        print(out)


if __name__ == '__main__':
    main()
