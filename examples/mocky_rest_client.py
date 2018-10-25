import logging
from urllib.parse import urljoin

from generic_rest_client.client import GenericRestClient

logger = logging.getLogger(__name__)


class MockyRestClient(GenericRestClient):
	def get_comments(self):
		"""
		Returns all the comments

		Returns:
			requests.models.Response: Response of the request
		"""

		endpoint_url = '/comments'

		return self.get_request(
			urljoin(self.base_url, endpoint_url),
			None,
			[200, ]
		)

	def new_post(self, params):
		"""
		Creates a new post

		Returns:
			requests.models.Response: Response of the request
		"""

		endpoint_url = '/posts'

		body_params = dict(
			title=params['title'],
			body=params['body'],
		)

		return self.post_request(
			urljoin(self.base_url, endpoint_url),
			body_params,
			[201, ]
		)

	def update_post(self, post_id, params):
		"""Updates an existing post

		Args:
			post_id(string): unique id of the post to be updated
			params(dict): new post information, this should contain:
				- title(str): New title
				- body(str): New body

		Returns:
			requests.models.Response: Response of the request
		"""

		endpoint_url = '/posts/{post_id}'.format(
			post_id=post_id,
		)

		body_params = dict(
			title=params['title'],
			body=params['body'],
		)

		return self.put_request(
			urljoin(self.base_url, endpoint_url),
			body_params,
			[200, ]
		)
