import logging

from generic_rest_client import GenericRestClient

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
			endpoint_url,
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
			endpoint_url,
			body_params,
			[201, ]
		)
