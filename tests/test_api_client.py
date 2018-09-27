import logging
from unittest import TestCase
from unittest import skip
from datetime import timedelta
import requests
import requests_mock

from django.conf import settings
from django.utils.timezone import now

from app.testing_helpers import override_django_setting
from app.testing_helpers import vcr
from app.tpaga_wallet_api_client import TpagaWalletRestClient
from app.api_client import RequestFailureException
from app.api_client import UnknownResultException


def get_http_client():
    api_conf = settings.TPAGA_WALLET_API_REST_CLIENT
    return TpagaWalletRestClient(
        base_url=api_conf['BASE_URL'],
        user=api_conf['USER'],
        password=api_conf['PASSWORD'],
    )


def valid_payment_request_params():
    return dict(
        miniapp_user_token='mauid-e67aee3b-85d9-4f4f-909c-79f8802cafdd',
        cost='1200',
        purchase_details_url='https://google.com',
        voucher_url='https://google.com',
        idempotency_token='110718-510pm',
        order_id='01',
        terminal_id='porgs!',
        purchase_description='vulptex',
        purchase_items=[dict(
            name='r2d2',
            value='456123',
        )],
        user_ip_address='127.0.0.1',
        expires_at=(now() + timedelta(days=30)).isoformat(),
    )


class TpagaWalletClientGetTestCase(TestCase):
    def test_connerror(self):
        with override_django_setting(
            'TPAGA_WALLET_API_REST_CLIENT.BASE_URL',
            'http://alderaan-do-not-exist.tpaga.co'
        ):
            client = get_http_client()

        with self.assertRaises(RequestFailureException) as ctx:
            client.get_request('', params={})

        self.assertIsNone(ctx.exception.response)

    @requests_mock.Mocker()
    def test_timeout(self, mock):
        mock.get(
            'https://stag.wallet.tpaga.co/alderaan',
            exc=requests.exceptions.Timeout,
        )
        client = get_http_client()

        with self.assertRaises(UnknownResultException) as ctx:
            client.get_request('alderaan', params={})

        self.assertIsNone(ctx.exception.response)


class TpagaWalletClientPostTestCase(TestCase):
    def test_connerror(self):
        with override_django_setting(
            'TPAGA_WALLET_API_REST_CLIENT.BASE_URL',
            'http://alderaan.tpaga.co'
        ):
            client = get_http_client()

        with self.assertRaises(RequestFailureException) as ctx:
            client.post_request('', body_params={})

        self.assertIsNone(ctx.exception.response)

    @requests_mock.Mocker()
    def test_timeout(self, mock):
        mock.post(
            'https://stag.wallet.tpaga.co/alderaan',
            exc=requests.exceptions.Timeout,
        )
        client = get_http_client()

        with self.assertRaises(UnknownResultException) as ctx:
            client.post_request('alderaan', body_params={})

        self.assertIsNone(ctx.exception.response)


class CreatePaymentRequestTestCase(TestCase):

    @vcr.use_cassette
    def test_create_payment_request_success(self):
        client = get_http_client()
        params = valid_payment_request_params()

        response = client.create_payment_request(params)
        self.assertEqual(response.status_code, 201)
        json = response.json()
        self.assertEqual(
            json['miniapp_user_token'],
            params['miniapp_user_token']
        )
        self.assertEqual(float(json['cost']), float(params['cost']))
        self.assertEqual(
            json['purchase_details_url'],
            params['purchase_details_url']
        )
        self.assertEqual(json['voucher_url'], params['voucher_url'])
        self.assertEqual(
            json['idempotency_token'],
            params['idempotency_token']
        )
        self.assertEqual(json['order_id'], params['order_id'])
        self.assertEqual(json['terminal_id'], params['terminal_id'])
        self.assertEqual(
            json['purchase_description'],
            params['purchase_description']
        )
        self.assertEqual(
            json['purchase_items']['name'],
            params['purchase_items'][0]['name']
        )
        self.assertEqual(
            json['user_ip_address'],
            params['user_ip_address']
        )
        self.assertFalse(json['merchant_user_id'])
        self.assertTrue(json['tpaga_payment_url'])
        self.assertEqual(json['status'], 'created')
        self.assertEqual(json['expires_at'], '2018-08-10T17:18:47.838-05:00')

    @vcr.use_cassette
    def test_duplicated_payment_request(self):
        client = get_http_client()
        params = valid_payment_request_params()

        response = client.create_payment_request(params)
        self.assertEqual(response.status_code, 409)
        json = response.json()
        self.assertEqual(
            json['miniapp_user_token'],
            params['miniapp_user_token']
        )
        self.assertEqual(float(json['cost']), float(params['cost']))
        self.assertEqual(
            json['purchase_details_url'],
            params['purchase_details_url']
        )
        self.assertEqual(json['voucher_url'], params['voucher_url'])
        self.assertEqual(
            json['idempotency_token'],
            params['idempotency_token']
        )
        self.assertEqual(json['order_id'], params['order_id'])
        self.assertEqual(json['terminal_id'], params['terminal_id'])
        self.assertEqual(
            json['purchase_description'],
            params['purchase_description']
        )
        self.assertEqual(
            json['purchase_items']['name'],
            params['purchase_items'][0]['name']
        )
        self.assertEqual(
            json['user_ip_address'],
            params['user_ip_address']
        )
        self.assertFalse(json['merchant_user_id'])
        self.assertTrue(json['tpaga_payment_url'])
        self.assertEqual(json['status'], 'created')
        self.assertEqual(
            json['expires_at'],
            '2018-08-10T17:18:47.838-05:00'
        )


class ObtainPaymentRequestInfoTestCase(TestCase):

    @vcr.use_cassette
    def test_obtain_payment_request_info_success(self):
        client = get_http_client()
        payment_request_token = 'pr-afe375f4349c3320b78fb65b305ff57a9c2e96333b0ad6d479f418f81dcbb8f98d92adde'
        params = valid_payment_request_params()

        response = client.obtain_payment_request_info(payment_request_token)
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(
            json['miniapp_user_token'],
            params['miniapp_user_token']
        )
        self.assertEqual(float(json['cost']), float(params['cost']))
        self.assertEqual(
            json['purchase_details_url'],
            params['purchase_details_url']
        )
        self.assertEqual(json['voucher_url'], params['voucher_url'])
        self.assertEqual(
            json['idempotency_token'],
            params['idempotency_token']
        )
        self.assertEqual(json['order_id'], params['order_id'])
        self.assertEqual(json['terminal_id'], params['terminal_id'])
        self.assertEqual(
            json['purchase_description'],
            params['purchase_description']
        )
        self.assertEqual(
            json['purchase_items']['name'],
            params['purchase_items'][0]['name']
        )
        self.assertEqual(json['user_ip_address'], params['user_ip_address'])
        self.assertFalse(json['merchant_user_id'])
        self.assertTrue(json['tpaga_payment_url'])
        self.assertEqual(json['status'], 'created')
        self.assertEqual(json['expires_at'], '2018-08-10T17:18:47.838-05:00')


class CancelPaymentRequestTestCase(TestCase):

    @vcr.use_cassette
    def test_cancel_non_existant_payment_request(self):
        client = get_http_client()
        payment_request_token = 'pr-helpmeimnotvalid'
        response = client.cancel_payment_request(payment_request_token)
        self.assertEqual(response.status_code, 422)

    @vcr.use_cassette
    def test_cancel_successful_payment_request(self):
        client = get_http_client()
        params = valid_payment_request_params()
        params['idempotency_token'] = 'cancel_success_token'
        response_created = client.create_payment_request(params)
        self.assertEqual(response_created.status_code, 201)
        json = response_created.json()
        self.assertEqual(json['status'], 'created')
        self.assertIsNone(json['cancelled_at'])

        payment_request_token = json['token']
        response = client.cancel_payment_request(payment_request_token)
        self.assertEqual(response.status_code, 200)
        json_cancelled = response.json()
        self.assertEqual(json_cancelled['status'], 'cancelled')
        self.assertEqual(json['token'], json_cancelled['token'])
        self.assertIsNotNone(json_cancelled['cancelled_at'])

        # Test duplicated cancellation
        response = client.cancel_payment_request(payment_request_token)
        self.assertEqual(response.status_code, 200)


class ObtainUserInformationTestCase(TestCase):

    @vcr.use_cassette
    def test_obtain_user_information_success(self):
        client = get_http_client()
        tpaga_user_token = 'mauid-2baff065-aa8a-46bb-9b5a-9280f1ccdcf0'

        response = client.obtain_user_information(tpaga_user_token)
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json['first_name'], 'Adela')
        self.assertEqual(json['last_name'], 'Rojass')
        self.assertEqual(json['phone_number'], '+573144009592')
        self.assertEqual(json['email'], 'arojas@tpaga.co')
        self.assertEqual(json['identification_type'], 'CC')
        self.assertEqual(json['identification_number'], '1618033988')

    @vcr.use_cassette
    def test_fail_invalid_user_(self):
        client = get_http_client()
        tpaga_user_token = 'mauid-alderaan456123'

        response = client.obtain_user_information(tpaga_user_token)
        self.assertEqual(response.status_code, 422)
        json = response.json()
        self.assertEqual(
            json['error_message'],
            'No se ha encontrado el usuario'
        )
        self.assertEqual(json['field_name'], 'tpaga_user_token')
        self.assertEqual(json['rejected_value'], tpaga_user_token)
