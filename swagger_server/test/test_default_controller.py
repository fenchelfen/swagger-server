# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.city_data import CityData  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_get_city_data_nonexisting_city(self):
        """Test case for get_city_data

        Response when the city doesn't exist
        """
        data = dict(name='name_example')
        response = self.client.open(
            'http://localhost:8080/city_name',
            method='POST',
            data=data,
            content_type='multipart/form-data')

        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertTrue(b'City not found' in response.data, 'Inconsistent response when the city doesn\'t exist')

    def test_get_city_data_existing_city(self):
        """Test case for get_city_data

        Response when the city doesn't exist
        """
        data = dict(name='Amsterdam')
        response = self.client.open(
            'http://localhost:8080/city_name',
            method='POST',
            data=data,
            content_type='multipart/form-data')

        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertTrue(b'"value": "United States of America"' in response.data,
                        'Inconsistent response when the city exists')


if __name__ == '__main__':
    import unittest

    unittest.main()
