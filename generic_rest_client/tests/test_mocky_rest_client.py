from unittest import TestCase

from examples.mocky_rest_client import MockyRestClient


def get_http_client():
	return MockyRestClient(
		base_url='https://jsonplaceholder.typicode.com/',
		user='',
		password='',
	)


class GetTestCase(TestCase):
	def setUp(self):
		self.client = get_http_client()

	def test_get_comments(self):
		response = self.client.get_comments()

		self.assertEqual(response.status_code, 200)
		json = response.json()
		self.assertTrue(len(json) > 1)
		item = json[0]
		self.assertIsNotNone(item['id'])
		self.assertIsNotNone(item['name'])
		self.assertIsNotNone(item['email'])

	def test_new_post(self):
		valid_params = dict(
			title='my first post',
			body='this is my first post',
		)

		response = self.client.new_post(
			params=valid_params,
		)

		self.assertEqual(response.status_code, 201)
		json = response.json()
		self.assertEqual(json['title'], valid_params['title'])
		self.assertEqual(json['body'], valid_params['body'])
