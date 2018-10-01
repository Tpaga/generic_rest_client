from unittest import TestCase

import requests
import requests_mock
from exceptions import RequestFailureException
from exceptions import UnknownResultException
from client import GenericRestClient

def get_http_client(base_url, user, password):
	return GenericRestClient(
		base_url=base_url,
		user=user,
		password=password,
	)


class GetTestCase(TestCase):
	def setUp(self):
		self.base_url = 'https://jsonplaceholder.typicode.com/'
		self.user = 'fake-user'
		self.password = 'fake-pass'
		self.client = get_http_client(
			base_url=self.base_url,
			user=self.user,
			password=self.password,
		)

	def test_connerror(self):
		client = get_http_client(
			base_url='http://alderaan-do-not-exist.tpaga.co',
			user=self.user,
			password=self.password,
		)

		with self.assertRaises(RequestFailureException) as ctx:
			client.get_request('', params={})

		self.assertIsNone(ctx.exception.response)

	@requests_mock.Mocker()
	def test_timeout(self, mock):
		mock.get(
			'https://jsonplaceholder.typicode.com/alderaan',
			exc=requests.exceptions.Timeout,
		)
		with self.assertRaises(UnknownResultException) as ctx:
			self.client.get_request('alderaan', params={})

		self.assertIsNone(ctx.exception.response)

	def test_successful_connection(self):
		response = self.client.get_request(
			'todos/1',
			params={},
			expected_http_codes=[200, ]
		)

		self.assertEqual(response.status_code, 200)
		json = response.json()
		self.assertEqual(json['userId'], 1)
		self.assertEqual(json['id'], 1)
		self.assertEqual(json['title'], 'delectus aut autem')
		self.assertEqual(json['completed'], False)


class ClientPostTestCase(TestCase):
	def setUp(self):
		self.base_url = 'https://jsonplaceholder.typicode.com/'
		self.user = 'fake-user'
		self.password = 'fake-pass'
		self.client = get_http_client(
			base_url=self.base_url,
			user=self.user,
			password=self.password,
		)

	def test_connerror(self):
		client = get_http_client(
			base_url='http://alderaan-do-not-exist.tpaga.co',
			user=self.user,
			password=self.password,
		)

		with self.assertRaises(RequestFailureException) as ctx:
			client.post_request('', body_params={})

		self.assertIsNone(ctx.exception.response)

	@requests_mock.Mocker()
	def test_timeout(self, mock):
		mock.post(
			'https://jsonplaceholder.typicode.com/alderaan',
			exc=requests.exceptions.Timeout,
		)
		with self.assertRaises(UnknownResultException) as ctx:
			self.client.post_request('alderaan', body_params={})

		self.assertIsNone(ctx.exception.response)

	def test_successful_connection(self):
		response = self.client.post_request(
			'posts',
			body_params=dict(
				name='tpaga rlz',
				author='manre',
			),
			expected_http_codes=[201, ]
		)

		self.assertEqual(response.status_code, 201)
		json = response.json()
		self.assertEqual(json['name'], 'tpaga rlz')
		self.assertEqual(json['author'], 'manre')
