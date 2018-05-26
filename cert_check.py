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
        self.domain = self._get_domain(url)
        if not self.domain:
            return

        cert = ssl.get_server_certificate((self.domain, 443))
        self.rcert = OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_PEM, cert)
        return all((self._verify_date(), self._verify_subject(owner)))

    def _get_domain(self, url):
        if url.startswith('http'):
            parsed = urlparser(url)
            return parsed.netloc
        else:
            print('URL must start with scheme (http / https)')
            return

    def _verify_date(self):
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
            return True

        print('Certificate has expired: %s - %s' % (not_before, not_after))
        self.logger.warning('Certificate has expired: %s - %s'
                            % (not_before, not_after))
        return

    def _verify_subject(self, org):
        subj_items = self.rcert.get_subject().get_components()
        org = ''
        cn = False
        for key, val in dict(list(subj_items)).items():
            val = val.decode('utf-8').lower()
            if key == b'O' and org.lower() in val:
                org = True

            if key == b'CN' and self.domain in val:
                cn = True

        return all((org, cn))
