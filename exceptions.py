import logging
from urllib.parse import urljoin

import requests
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)


class RequestFailureException(Exception):
    """Raised when the request did *not* succeed, and we know nothing happened
    in the remote side. From a businness-logic point of view, the operation the
    client was supposed to perform did NOT happen"""

    def __init__(self, *args, url='', response=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.response = response
        self.url = url


class UnknownResultException(Exception):
    """Raised when we don't know if the request was completed or not. From a
    businness-logic point of view, it is not known if the operation succeded,
    or failed"""

    def __init__(self, *args, url='', response=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.response = response
        self.url = url


class GenericRestClient:

    request_failure_exception = RequestFailureException
    unknown_failure_exception = UnknownResultException

    def __init__(
        self,
        base_url,
        user,
        password,
        timeout=10,
    ):
        self.base_url = base_url
        self.user = user
        self.password = password
        self.auth = HTTPBasicAuth(self.user, self.password)
        self.timeout = timeout
        self.headers = {
            "Accept": "application/json",
            "content-type": "application/json",
        }

    def do_request(self, endpoint, params, call_type, expected_http_codes):
        """Create a payload and send a new post request to the url given

        Args:
            endpoint (string): portion of the endpoint for the service
            params (dict): a valid data object
            call_type (string): one of "get" or "post"
            expected_http_codes list(int): expected codes for the request

        Raises:
            RequestFailureException
            UnknownResultException
        Returns:
            The response offered by the requests library when using get or post
        """
        url = urljoin(self.base_url, endpoint)
        try:
            if call_type == "get":
                response = requests.get(
                    url,
                    params=params,
                    headers=self.headers,
                    auth=self.auth,
                    timeout=self.timeout,
                )
            elif call_type == "post":
                response = requests.post(
                    url,
                    json=params,
                    headers=self.headers,
                    auth=self.auth,
                    timeout=self.timeout,
                )
        except requests.exceptions.ConnectionError as exc:
            logger.error(
                'Could not connect to API',
                extra={
                    'url': url,
                    'request_body': params,
                    'timeout': self.timeout,
                    'exception': exc,
                },
            )
            raise self.request_failure_exception(url=url) from exc
        except requests.exceptions.Timeout as exc:
            logger.error(
                'Timeout in request to API',
                extra={
                    'url': url,
                    'request_body': params,
                    'timeout': self.timeout,
                    'exception': exc,
                },
            )
            raise self.unknown_failure_exception(url=url) from exc

        if expected_http_codes is None:
            expected_http_codes = [200, ]
        if response.status_code in expected_http_codes:
            return response

        if response.status_code >= 400 and response.status_code < 500:
            errmsg = 'API returned HTTP 4xx error'

            logger.error(errmsg, extra={
                'url': url,
                'request_body': params,
                'response_status_code': response.status_code,
                'response_body': response.content,
            })
            raise self.request_failure_exception(
                url=url, response=response
            )

        if response.status_code >= 500:
            logger.error('API REST returned HTTP 5xx error', extra={
                'url': url,
                'request_body': params,
                'response_status_code': response.status_code,
                'response_body': response.content,
            })
            raise self.unknown_failure_exception(
                url=url, response=response,
            )

        logger.error(
            'Unexpected status code in response from API',
            extra={
                'url': url,
                'request_body': params,
                'response_status_code': response.status_code,
                'response_body': response.content,
            }
        )

        raise self.request_failure_exception(
            url=url, response=response,
        )

    def get_request(self, endpoint, params, expected_http_codes=None):
        """Create a payload and send a new post request to the given url

        Args:
            endpoint (string): portion of the endpoint for the service
            params (dict): a valid data object
            expected_http_codes list(int): expected codes for the request
        Returns:
            The response offered by the requests library when using get
        """
        return self.do_request(endpoint, params, 'get', expected_http_codes)

    def post_request(self, endpoint, body_params, expected_http_codes=None):
        """Create a payload and send a new post request to the given url

        Args:
            endpoint (string): portion of the endpoint for the service
            body_params (dict): a valid data object
            expected_http_codes list(int): expected codes for the request
        Returns:
            The response offered by the requests library when using post
        """
        return self.do_request(
            endpoint,
            body_params,
            'post',
            expected_http_codes
        )
