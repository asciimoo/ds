from ds import select, parse_query
from unittest import TestCase, main

d1 = [{'a': 1}, {'a': 2.0, 'b': 3}]

d2 = {'asdf': 'wqer', 'zxcv': {'a': 1, 'b': 3}, 'poiu': [1, 1.1, 'mnbv', '"asdf"']}


class QueryParseTestCase(TestCase):

    def test_one_field(self):
        self.assertEqual(parse_query('/asdf'), [{'type': None, 'name': 'asdf'}])

    def test_two_fields(self):
        self.assertEqual(parse_query('/asdf/qwer'), [{'type': None, 'name': 'asdf'},
                                                     {'type': None, 'name': 'qwer'}])

    def test_quoted(self):
        self.assertEqual(parse_query('/"asdf/qwer"'), [{'type': None, 'name': 'asdf/qwer'}])

    def test_type(self):
        self.assertEqual(parse_query('/<str>'), [{'type': 'str', 'name': ''}])

    def test_type_and_name(self):
        self.assertEqual(parse_query('/<float>asdf'), [{'type': 'float', 'name': 'asdf'}])


class SelectTestCase(TestCase):

    def test_one(self):
        self.assertEqual(select(d1, '/a'), [1, 2])

    def test_two(self):
        self.assertEqual(select(d2, '/zxcv/a'), [1])

    def test_index(self):
        self.assertEqual(select(d1, '/0'), [{'a': 1}])

    def test_type(self):
        self.assertEqual(select(d1, '/<int>'), [1, 3])

    def test_type_index(self):
        self.assertEqual(select(d2, '/<list>/2'), ['mnbv'])


if __name__ == '__main__':
    main()
