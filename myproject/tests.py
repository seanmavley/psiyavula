from unittest import TestCase
from .views import my_view, result_view
from pyramid import testing
from selenium import webdriver
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class ViewTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        request = testing.DummyRequest()
        response = my_view(request)
        self.assertEqual(response['project'], 'MyProject')
        # self.assertEqual(response.status_code, 200)

    def test_POST_of_view(self):
        request = testing.DummyRequest('/', params={'url': 'http://en.wikipedia.org/wiki/Thomas_Mensah'}, post=True)
        response = result_view(request)

        # according to 
        # http://docs.pylonsproject.org/projects/pyramid/en/master/quick_tutorial/unit_testing.html#qtut-unit-testing
        # response.status_code below should output an int as return value
        # No idea yet, why that doesn't work.
        self.assertEqual(response.status_code, 200)


class TestViaBrowser(TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(os.path.join(BASE_DIR, 'chromedriver'))
        self.browser.implicitly_wait(3)
        # time.sleep(5)

    def tearDown(self):
        self.browser.quit()

    def test_input(self):
        self.browser.get('http://localhost:6543/')

        # Check if input field is required.
        required = self.browser.find_element_by_xpath("//input[@required]")
        # Check if there's a reset button
        reset = self.browser.find_element_by_xpath("//input[@type='reset']")
        # try submitting form
        input_box = self.browser.find_element_by_id('url')
        input_box.send_keys('http://en.wikipedia.org/wiki/Thomas_Mensah')
        input_box.submit()
