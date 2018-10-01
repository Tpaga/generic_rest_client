# Tests

Tests are stored into the tests/ folder, to run all the tests:

    python -m unittest discover tests

To run an individual test:

    python -m unittest tests/test_api_client.py

# Publish

If you want to publish a new version you must

    python setup.py upload
