import os
from unittest import TestCase

import OpenSSL

from apiist import ssl_adapter
from apiist.http import http
from tests.unit import RESOURCES_DIR


class CryptoMock:
    class PKCS12:
        class CertMock:
            def __init__(self, cert):
                self.certificate = cert

            def get_notAfter(self):
                return b'30211126001957Z'

        def __init__(self):
            self.privatekey = None
            self.certificate = None

        def set_privatekey(self, key):
            self.privatekey = key

        def set_certificate(self, cert):
            self.certificate = cert

        def get_certificate(self):
            return self.CertMock(self.certificate)

        def get_ca_certificates(self):
            return []

        def get_privatekey(self):
            return self.privatekey

    def __init__(self):
        self.FILETYPE_PEM = 'pem'
        self.load_pkcs12_called = 0
        self.load_certificate_called = 0
        self.load_privatekey_called = 0

    def load_certificate(self, filetype, data):
        self.load_certificate_called += 1

        return 'certificate'

    def load_privatekey(self, filetype, data, passphrase):
        self.load_privatekey_called += 1

        return 'privatekey'

    def load_pkcs12(self, data, password):
        self.load_pkcs12_called += 1

        pkcs12 = self.PKCS12()
        pkcs12.certificate = 'certificate'
        pkcs12.privatekey = 'privatekey'
        return pkcs12


class PyOpenSSLContextMock:
    class ContextMock:
        def __init__(self):
            self.certificate = None
            self.privatekey = None
            self.chain_certificates = []

        def use_certificate(self, cert):
            self.certificate = cert

        def add_extra_chain_cert(self, cert):
            self.chain_certificates.append(cert)

        def use_privatekey(self, key):
            self.privatekey = key

    def __init__(self, ssl_protocol):
        self._ctx = self.ContextMock()
        self.ssl_protocol = ssl_protocol


class TestSSLAdapter(TestCase):
    def setUp(self):
        self.real_crypto = ssl_adapter.crypto
        self.real_PyOpenSSLContext = ssl_adapter.PyOpenSSLContext
        ssl_adapter.crypto = CryptoMock()
        ssl_adapter.PyOpenSSLContext = PyOpenSSLContextMock

    def tearDown(self):
        ssl_adapter.crypto = self.real_crypto
        ssl_adapter.PyOpenSSLContext = self.real_PyOpenSSLContext

    def test_adapter_with_p12_cert(self):
        certificate_file_path = os.path.join(RESOURCES_DIR, "certificates/dump-file.p12")
        adapter = ssl_adapter.SSLAdapter(certificate_file_path=certificate_file_path, passphrase='pass')

        self.assertEqual('privatekey', adapter.ssl_context._ctx.privatekey)
        self.assertEqual('certificate', adapter.ssl_context._ctx.certificate.certificate)
        self.assertEqual(1, ssl_adapter.crypto.load_pkcs12_called)
        self.assertEqual(0, ssl_adapter.crypto.load_certificate_called)
        self.assertEqual(0, ssl_adapter.crypto.load_privatekey_called)

    def test_adapter_with_pem_cert(self):
        certificate_file_path = os.path.join(RESOURCES_DIR, "certificates/dump-file.pem")
        adapter = ssl_adapter.SSLAdapter(certificate_file_path=certificate_file_path, passphrase='pass')

        self.assertEqual('privatekey', adapter.ssl_context._ctx.privatekey)
        self.assertEqual('certificate', adapter.ssl_context._ctx.certificate.certificate)
        self.assertEqual(0, ssl_adapter.crypto.load_pkcs12_called)
        self.assertEqual(1, ssl_adapter.crypto.load_certificate_called)
        self.assertEqual(1, ssl_adapter.crypto.load_privatekey_called)


# TODO: This class contains integration tests. Need to be removed in future
class TestSSL(TestCase):
    def setUp(self):
        self.host = 'client.badssl.com'
        self.request_url = 'https://client.badssl.com/'
        self.certificate_file_pem = os.path.join(RESOURCES_DIR, "certificates/badssl.com-client.pem")
        self.certificate_file_p12 = os.path.join(RESOURCES_DIR, "certificates/badssl.com-client.p12")
        self.passphrase = 'badssl.com'

    def test_get_with_encrypted_p12_certificate(self):
        encrypted_cert = (self.certificate_file_p12, self.passphrase)
        response = http.get(self.request_url, encrypted_cert=encrypted_cert)
        self.assertEqual(200, response.status_code)

    def test_get_with_encrypted_pem_certificate(self):
        encrypted_cert = (self.certificate_file_pem, self.passphrase)
        response = http.get(self.request_url, encrypted_cert=encrypted_cert)
        self.assertEqual(200, response.status_code)

    def test_get_with_incorrect_certificate(self):
        certificate_file_pem_incorrect = os.path.join(RESOURCES_DIR, "certificates/badssl.com-client-wrong.pem")
        encrypted_cert = (certificate_file_pem_incorrect, self.passphrase)
        response = http.get(self.request_url, encrypted_cert=encrypted_cert)
        self.assertEqual(400, response.status_code)

    def test_get_with_incorrect_secret(self):
        wrong_certificate_secret = 'you shall not pass'
        encrypted_cert = (self.certificate_file_pem, wrong_certificate_secret)
        self.assertRaises(OpenSSL.crypto.Error, http.get, self.request_url, encrypted_cert=encrypted_cert)

    def test_get_with_ssl_and_wrong_url(self):
        cert_missing_url = 'https://client-cert-missing.badssl.com/'
        encrypted_cert = (self.certificate_file_p12, self.passphrase)
        response = http.get(cert_missing_url, encrypted_cert=encrypted_cert)
        self.assertEqual(400, response.status_code)
