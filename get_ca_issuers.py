#!/usr/local/bin env

import requests

class CAIssuersParser:
    '''Parses list of CA's from Mozilla, Chrome, Opera, iOS.'''

    # https://en.wikipedia.org/wiki/Certificate_authority#Providers

    CA_LISTS = {
        'mozilla': {
            'list': ''.join([
                'https://hg.mozilla.org/releases/mozilla-beta/raw-file/',
                'tip/security/nss/lib/ckfw/builtins/certdata.txt',
            ]),
            'pattern': '# Issuer ',
        }
    }
    ISSUERS = []

    # TODO: parse the other lists and store the CA's into a file
    def parse_issuers(self):
        resp = requests.get(self.CA_LISTS['mozilla']['list'])
        raw_list = resp.text
        pattern = self.CA_LISTS['mozilla']['pattern']
        for line in raw_list.split('\n'):
            if line.startswith(pattern):
                issuer = line.lstrip(pattern)
                if issuer not in self.ISSUERS:
                    print(issuer)
                    self.ISSUERS.append(issuer)
