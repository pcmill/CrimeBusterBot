#!/usr/local/bin env

import binascii
import datetime
import logging
import OpenSSL
import pytz
import re
import ssl
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from urllib.parse import urlparse as urlparser


class CertChecker:
    '''Verifies the TLS/SSL certificate of a website.'''

    # common fields:
    # https://en.wikipedia.org/wiki/Public_key_certificate#Common_fields

    # example code:
    # https://www.programcreek.com/python/example/62606/ssl.get_server_certificate

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

        # try this: https://github.com/fschulze/check-tls-certs/blob/master/check_tls_certs.py#L59-L71
        cert = ssl.get_server_certificate((self.domain, 443))
        self.rcert = OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_PEM, cert)
        self._get_extensions()
        return all((
            self._verify_date(),
            self._verify_subject(owner),
            #self._verify_issuer(),  # WIP
        ))

    def _get_extensions(self, content):
        '''Gets data from extensions.'''

        exts = content.extensions
        # extensions is an array
        # extensions can be extracted using OID, list of OID's:
        # https://cryptography.io/en/latest/x509/reference/#object-identifiers


    def _get_content(self):
        '''Decrypts certificate and returns its content.'''

        # https://stackoverflow.com/a/16899645
        cert = ssl.get_server_certificate((self.domain, 443))
        bycert = cert.encode('utf-8')
        return x509.load_pem_x509_certificate(bycert, default_backend())

    def _get_domain(self, url):
        if url.startswith('http'):
            parsed = urlparser(url)
            return parsed.netloc
        else:
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
        self.logger.debug(issuer_comp)
        return


if __name__ == '__main__':
    CertChecker().check('https://google.com', 'google.com')
