import json
import unittest
import requests

region_url = 'https://regions-test.maps.com/1.0/regions'


def return_regions(url):
    body = json.loads(requests.get(url).content)
    return body


class TestSearch(unittest.TestCase):
    def test_search_min(self):
        error_entry = list(return_regions(region_url + '?q=ск'))[0]
        self.assertEqual(error_entry, 'error')
        error_entry = list(return_regions(region_url + '?q=с'))[0]
        self.assertEqual(error_entry, 'error')
        self.assertNotEqual(requests.get(region_url + '?q=').status_code, '200')

    def test_search_register(self):
        list_of_ids_1 = []
        for element in return_regions(region_url + '?q=рск')['items']:
            list_of_ids_1.append(element['id'])
        list_of_ids_2 = []
        for element in return_regions(region_url + '?q=РСК')['items']:
            list_of_ids_2.append(element['id'])
        self.assertEqual(list_of_ids_1, list_of_ids_2)

    def test_search_sole_param(self):
        list_of_ids_1 = []
        for element in return_regions(region_url + '?q=рск')['items']:
            list_of_ids_1.append(element['id'])
        list_of_ids_2 = []
        for element in return_regions(region_url + '?country_code=ru&page=2&page_size=5&q=рск&')['items']:
            list_of_ids_2.append(element['id'])
        self.assertEqual(list_of_ids_1, list_of_ids_2)


class TestCountryCode(unittest.TestCase):

    def test_country_code_ru(self):
        list_of_items = return_regions(region_url + '?country_code=ru')['items']
        for element in list_of_items:
            self.assertEqual(element['country']['code'], 'ru')

    def test_country_code_kg(self):
        list_of_items = return_regions(region_url + '?country_code=kg')['items']
        for element in list_of_items:
            self.assertEqual(element['country']['code'], 'kg')

    def test_country_code_kz(self):
        list_of_items = return_regions(region_url + '?country_code=kz')['items']
        for element in list_of_items:
            self.assertEqual(element['country']['code'], 'kz')

    def test_country_code_cz(self):
        list_of_items = return_regions(region_url + '?country_code=cz')['items']
        for element in list_of_items:
            self.assertEqual(element['country']['code'], 'cz')

    def test_country_code_default(self):
        list_of_items = return_regions(region_url)['items']
        for element in list_of_items:
            self.assertIn(element['country']['code'], ['kg', 'kz', 'ru', 'cz'])

    def test_country_code_other(self):
        error_entry = list(return_regions(region_url + '?country_code=1@'))[0]
        self.assertEqual(error_entry, 'error')

    def test_country_code_null(self):
        error_entry = list(return_regions(region_url + '?country_code='))[0]
        self.assertEqual(error_entry, 'error')


class TestPageNumber(unittest.TestCase):
    def test_page_zero(self):
        self.assertNotEqual(requests.get(region_url + '?page=0').status_code, '200')

    def test_page_default(self):
        list_of_ids_1 = []
        for element in return_regions(region_url)['items']:
            list_of_ids_1.append(element['id'])
        list_of_ids_2 = []
        for element in return_regions(region_url + '?page=1')['items']:
            list_of_ids_2.append(element['id'])
        self.assertEqual(list_of_ids_1, list_of_ids_2)

    def test_page_invalid(self):
        error_entry = list(return_regions(region_url + '?page=1.2a'))[0]
        self.assertEqual(error_entry, 'error')


class TestPageSize(unittest.TestCase):
    def test_page_size_5(self):
        list_of_items = return_regions(region_url + '?page_size=5')['items']
        self.assertEqual(len(list_of_items), 5)

    def test_page_size_10(self):
        list_of_items = return_regions(region_url + '?page_size=10')['items']
        self.assertEqual(len(list_of_items), 10)

    def test_page_size_15(self):
        list_of_items = return_regions(region_url + '?page_size=15')['items']
        self.assertEqual(len(list_of_items), 15)

    def test_page_size_default(self):
        list_of_items = return_regions(region_url)['items']
        self.assertEqual(len(list_of_items), 15)

    def test_page_size_invalid(self):
        error_entry = list(return_regions(region_url + '?page_size=7'))[0]
        self.assertEqual(error_entry, 'error')


if __name__ == '__main__':
    unittest.main(verbosity=2)
