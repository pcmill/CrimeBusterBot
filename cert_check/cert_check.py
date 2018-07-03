#!/usr/local/bin env

import datetime
import logging
import pytz
import ssl
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from urllib.parse import urlparse as urlparser


class CertChecker:
    '''Verifies the TLS/SSL certificate of a website.'''

    logger = logging.getLogger('cbb.cert-check')

    def __init__(self, url):
        # see also https://stackoverflow.com/a/7691293
        self.domain = self._get_domain(url)
        self.content = self._get_content()

    def check(self):
        '''Main publick check function.'''
        print('\n\n Initialising TLS/SSL certificate check ...')
        if not self.domain:
            return

        return all((
            self._verify_version(),
            self._verify_date(),
            self._verify_subject(),
#            self._verify_issuer(),
            self._get_extensions(),
        ))

    def _get_domain(self, url):
        '''Extracts domain name from the URL.'''
        print('\n Getting domain ...')
        if url.startswith('http'):
            parsed = urlparser(url)
            domain = parsed.netloc
            print('Domain: {0}'.format(domain))
            return domain
        else:
            self.logger.warning('URL must start with scheme (http / https)')
            return

    def _get_content(self):
        '''Decrypts certificate and returns `Certificate` object.
        See https://cryptography.io/en/latest/x509/reference/#x-509-certificate-object
        for more details.
        '''  # noqa: E501
        print('\n Getting certificate ...')
        # https://stackoverflow.com/a/16899645
        cert = ssl.get_server_certificate((self.domain, 443))
        bycert = cert.encode('utf-8')
        content = x509.load_pem_x509_certificate(bycert, default_backend())
        print(content)
        return content

    def _verify_version(self):
        '''Verifies certificate version.'''
        print('\n Verifying certificate version ...')
        try:
            version = self.content.version
            print('Version: {0}'.format(version))
            return True
        except x509.InvalidVersion as ex:
            print('Invalid certificate version: {0}'.format(ex))
            self.logger.warning('Invalid certificate version: {0}'.format(ex))
            return

    def _verify_date(self):
        '''Verifies certificate date.'''
        print('\n Verifying certificate dates ...')
        # get notBefore
        not_before = self.content.not_valid_before
        # get notAfter
        not_after = self.content.not_valid_after
        # check the cert
        if (not_before <= datetime.datetime.utcnow() < not_after):
            print('Dates - OK')
            return True

        print('Certificate has expired: %s - %s' % (not_before, not_after))
        self.logger.warning('Certificate has expired: %s - %s'
                            % (not_before, not_after))
        return

    # TODO
    def _verify_subject(self):
        print('\n Verifying certificate subject ...')
        for attribute in self.content.subject:
            key = attribute.oid._name
            val = attribute.value
            print('{0}: {1}'.format(key, val))
            # check if domain name coinsides with the Common Name
            if key == 'commonName' and self.domain.lower() in val.lower():
                print(self.domain, val)
                return True

        return

    # TODO
    def _get_extensions(self):
        '''Gets data from extensions.'''
        print('\n Verifying certificate extensions ...')
        san = self.content.extensions.get_extension_for_class(
            x509.SubjectAlternativeName)
        print('SAN: {0}'.format(san.value.get_values_for_type(x509.DNSName)))

    # TODO
    def _verify_issuer(self):
        # http://www.sos.ca.gov/administration/regulations/current-regulations/technology/digital-signatures/approved-certification-authorities/
        print('\n Verifying certificate issuer ...')
        for attribute in self.content.issuer:
            key = attribute.oid._name
            val = attribute.value
            print('{0}: {1}'.format(key, val))


if __name__ == '__main__':
    CertChecker('https://google.com').check()
    CertChecker('https://yahoo.com').check()
#    CertChecker('http://admkant.nl/').check()
