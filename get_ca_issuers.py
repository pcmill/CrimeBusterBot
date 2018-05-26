#!/usr/local/bin env

import requests

class CAIssuersParser:
    '''Parses list of CA's from Mozilla, Chrome, Opera, iOS.'''

    # https://en.wikipedia.org/wiki/Certificate_authority#Providers

    URLS = [
        'https://hg.mozilla.org/releases/mozilla-beta/raw-file/tip/security/nss/lib/ckfw/builtins/certdata.txt',
    ]
    ISSUERS = []

    def parse_issuers(self):
        resp = requests.get(self.URLS[0])
        raw_list = resp.text
        pattern = '# Issuer: '
        for line in raw_list.split('\n'):
            if line.startswith(pattern):
                issuer = line.lstrip(pattern)
                if issuer not in self.ISSUERS:
                    print(issuer)
                    self.ISSUERS.append(issuer)
