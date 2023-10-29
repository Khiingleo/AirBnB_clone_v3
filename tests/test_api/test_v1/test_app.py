#!/usr/bin/python3
"""
    Test for api/v1/app.py
"""
from api.v1 import app
import inspect
import pep8
import unittest


class TestAppsDocs(unittest.TestCase):
    """ A class for testing the api's app docs """

    all_methods = inspect.getmembers(app, inspect.isfunction)

    def test_app_file(self):
        """ checking documentation for the app's file """
        actual = app.__doc__
        self.assertIsNotNone(actual)

    def test_all_docs(self):
        """ Checking all docs of all function in app """
        app_functions = TestAppsDocs.all_methods
        for a_function in app_functions:
            self.assertIsNotNone(a_function[1].__doc__)

    
    def test_app_pep8(self):
        """ Checking if app.py is PEP8 compliant """
        pep8_style = pep8.StyleGuide(quite=True)
        errors = pep8_style.check_files(['api/v1/app.py'])
        self.assertEqual(errors.total_errors, 0, errors.messages)


if __name__ == "__main__":
    """ Run main """
    unittest.main
