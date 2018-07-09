#!/bin/env python3

import datetime
import logging
import pytz
import requests
import ssl
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from urllib.parse import urlparse as urlparser


class CertChecker:
    '''Verifies the TLS/SSL certificate of a website.'''

    logger = logging.getLogger('cbb.cert-check')
    logger.setLevel('INFO')

    def __init__(self, url):
        # see also https://stackoverflow.com/a/7691293
        self.url = url
        print(requests.get(self.url))

        self.domain = self._get_domain()
        self.content = self._get_content()

    def check(self):
        '''Main public check function.'''
        self.logger.info('Initialising TLS/SSL certificate check ...')
        if not self.domain:
            return

        return all((
            self._verify_version(),
            self._verify_date(),
            self._verify_subject(),
#            self._verify_issuer(),
            self._get_extensions(),
        ))

    def _get_domain(self):
        '''Extracts domain name from the URL.'''
        self.logger.info('Getting domain ...')
        parsed = urlparser(self.url)
        if parsed.netloc:
            domain = parsed.netloc
        else:
            self.logger.warning('URL must start with scheme (http / https).')
            url = '//{0}'.format(self.url)
            parsed = urlparser(url)
            domain = parsed.netloc
            if not domain:
                self.logger.error(
                    'Error while parsing the URL. Check the format.')
                return

        self.logger.info('Domain: {0}'.format(domain))
        print(domain)
        return domain

    def _get_content(self):
        '''Decrypts certificate and returns `Certificate` object.
        See https://cryptography.io/en/latest/x509/reference/#x-509-certificate-object
        for more details.
        '''  # noqa: E501
        self.logger.info('Getting certificate ...')
        print('Getting certificate ...')
        # https://stackoverflow.com/a/16899645
        cert = ssl.get_server_certificate((self.domain, 443))
        print('cert done')
        bycert = cert.encode('utf-8')
        print('bcert done')
        content = x509.load_pem_x509_certificate(bycert, default_backend())
        self.logger.info(content)
        print('Done')
        return content

    def _verify_version(self):
        '''Verifies certificate version.'''
        self.logger.info('Verifying certificate version ...')
        print('Verifying certificate version ...')
        try:
            version = self.content.version
            self.logger.info('Version: {0}'.format(version))
            print('Done')
            return True
        except x509.InvalidVersion as ex:
            self.logger.warning('Invalid certificate version: {0}'.format(ex))
            print('Invalid certificate version: {0}'.format(ex))
            return

    def _verify_date(self):
        '''Verifies certificate date.'''
        self.logger.info('Verifying certificate dates ...')
        print('Verifying certificate dates ...')
        # get notBefore
        not_before = self.content.not_valid_before
        # get notAfter
        not_after = self.content.not_valid_after
        # check the cert
        if not_before <= datetime.datetime.utcnow() < not_after:
            self.logger.info('Dates - OK')
            print('Done')
            return True

        self.logger.warning('Certificate has expired: %s - %s'
                            % (not_before, not_after))
        print('Certificate has expired: %s - %s'
                            % (not_before, not_after))
        return

    # TODO
    def _verify_subject(self):
        self.logger.info('Verifying certificate subject ...')
        print('Verifying certificate subject ...')
        for attribute in self.content.subject:
            key = attribute.oid._name
            val = attribute.value
            self.logger.info('{0}: {1}'.format(key, val))
            print('{0}: {1}'.format(key, val))
            # check if domain name coinsides with the Common Name
            if key == 'commonName' and self.domain.lower() in val.lower():
                self.logger.info(self.domain, val)
                print('Done')
                return True

        return

    # TODO
    def _get_extensions(self):
        '''Gets data from extensions.'''
        self.logger.info('Verifying certificate extensions ...')
        san = self.content.extensions.get_extension_for_class(
            x509.SubjectAlternativeName)
        self.logger.info(
            'SAN: {0}'.format(san.value.get_values_for_type(x509.DNSName)))
        print(
            'SAN: {0}'.format(san.value.get_values_for_type(x509.DNSName)))
        return True

    # TODO
    def _verify_issuer(self):
        # http://www.sos.ca.gov/administration/regulations/current-regulations/technology/digital-signatures/approved-certification-authorities/
        self.logger.info('Verifying certificate issuer ...')
        for attribute in self.content.issuer:
            key = attribute.oid._name
            val = attribute.value
            self.logger.info('{0}: {1}'.format(key, val))
