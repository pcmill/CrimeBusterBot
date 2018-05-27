#!/usr/local/bin env

import datetime
import logging
import OpenSSL
import pytz
import ssl
from urllib.parse import urlparse as urlparser


class CertChecker:
    '''Verifies the TLS/SSL certificate of a website.'''

    # common fields:
    # https://en.wikipedia.org/wiki/Public_key_certificate#Common_fields

    logger = logging.getLogger('cert-check')

    def __init__(self):
        # see also https://stackoverflow.com/a/7691293
        self.rcert = None
        self.domain = None

    def check(self, url, owner):
        print('Initialising TLS/SSL certificate check ...')
        self.domain = self._get_domain(url)
        if not self.domain:
            return

        cert = ssl.get_server_certificate((self.domain, 443))
        self.rcert = OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_PEM, cert)
        return all((
            self._verify_date(),
            self._verify_subject(owner),
            #self._verify_issuer(),  # not implemented
        ))

    def _get_domain(self, url):
        if url.startswith('http'):
            parsed = urlparser(url)
            return parsed.netloc
        else:
            print('URL must start with scheme (http / https)')
            self.logger.warning('URL must start with scheme (http / https)')
            return

    def _verify_date(self):
        print('Verifying certificate dates ...')
        utc = pytz.UTC
        # get notBefore
        not_before_str = self.rcert.get_notBefore().decode('utf-8')
        not_before_naive = datetime.datetime.strptime(not_before_str,
                                                      '%Y%m%d%H%M%SZ')
        not_before = not_before_naive.replace(tzinfo=utc)
        # get notAfter
        not_after_str = self.rcert.get_notAfter().decode('utf-8')
        not_after_naive = datetime.datetime.strptime(not_after_str,
                                                     '%Y%m%d%H%M%SZ')
        not_after = not_after_naive.replace(tzinfo=utc)
        # check the cert
        if (not_before <= datetime.datetime.now(pytz.timezone('UTC'))
                < not_after):
            print('Dates - OK')
            return True

        print('Certificate has expired: %s - %s' % (not_before, not_after))
        self.logger.warning('Certificate has expired: %s - %s'
                            % (not_before, not_after))
        return

    def _verify_subject(self, org):
        print('Verifying certificate subject ...')
        subj_items = self.rcert.get_subject().get_components()
        org = ''
        cn = False
        for key, val in dict(subj_items).items():
            val = val.decode('utf-8').lower()
            if key == b'O' and org.lower() in val:
                print('Organisation - OK')
                org = True

            if key == b'CN' and self.domain in val:
                print('Domain - OK')
                cn = True

        return all((org, cn))

    # TODO
    def _verify_issuer(self):
        issuer_obj = self.rcert.get_issuer()
        issuer_comp = issuer_obj.get_components()#.decode('utf-8')
        print(issuer_comp)
        return
