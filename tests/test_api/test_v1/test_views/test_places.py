#!/usr/bin/python3
"""
    The Unittest for api/v1/views/place
"""
import inspect
import pep8
import web_flask
import unittest
from os import stat
import api
places_module = api.v1.views.places


class TestPlacesDocs(unittest.TestCase):
    """ Checking docs for places endpoint """

    all_methods = inspect.getmembers(places_module, inspect.isfunction)


    def test_places_doc(self):
        """ Checking the documentation of docs file """
        places_doc = places_module.__doc__
        self.assertIsNotNone(places_doc)

     def test_places_pep8(self):
         """ Checking if places is pep8 compliant """
         pep8_style = pep8.StyleGuide(quite=True)
         errors = pep8style.check_files(['api/v1/views/places.py'])
         self.assertEqual(errors.total_errors, 0, errors.messages)

    def test_places_function_docs(self):
        """ Checking if all funcitions in places have documentation """
        places_functions = TestPlacesDocs.all_methods
        for a_function in places_function:
            self.assertIsNotNone(a_function[1].__doc__)

    def test_if_file_executable(self):
        """ Checking if places file is executable """
        places_status = stat('api/v1/views/places.py')
        permissions = str(oct(places_status[0]))
        executable = int(permissions[5:-2]) >= 5
        self.assertTrue(executable)

