'''
ds is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ds is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with ds. If not, see < http://www.gnu.org/licenses/ >.

(C) 2014- by Adam Tauber, <asciimoo@gmail.com>
'''

try:
    from future_builtins import map, filter
except:
    pass
import re
from collections import Iterable

from sys import version_info
IS_PY3 = version_info[0] == 3

if IS_PY3:
    unicode = str


grammar = re.compile(r"""/(?:
([^/"]+)|
"(.+)"
)""", re.U | re.VERBOSE)

field_type_regex = re.compile(r'^<(?P<type>[^>]+)>.*$', re.U)

type_map = {'int': (int,),
            'integer': (int,),
            'bool': (bool,),
            'boolean': (bool,),
            'str': (str, unicode),
            'string': (str, unicode),
            'float': (float, ),
            'list': (list, tuple),
            'dict': (dict,)}


class QueryParseException(Exception):
    """Exception raised when a query string can not be parsed."""
    pass


def iterate(iterable):
    if type(iterable) == dict:
        it = iterable.items()

    else:
        it = enumerate(iterable)

    for index, value in it:
        if type(index) == int:
            index = str(index)
        yield index, value


def is_iterable(obj):
    if type(obj) == str:
        return False

    if type(obj) == unicode:
        return False

    return isinstance(obj, Iterable)


def parse_field(field):
    field_type = None

    m = field_type_regex.match(field)
    if m:
        field_type = m.group('type')
        field = field.replace('<{0}>'.format(field_type), '', 1)

    return {'type': field_type,
            'name': field}


def parse_query(query):
    matches = grammar.findall(query)

    if not matches:
        raise QueryParseException("wrong query")

    fields = list(map(parse_field,
                      [first(filter(None, match)) for match in matches]))

    return fields


def type_check(value, type_name):
    if not type_name:
        return True

    return (type(value) in type_map.get(type_name, tuple())
            or value.__class__.__name__ == type_name)


def first(iterable):
    if type(iterable) == list:
        return iterable[0]
    return next(iterable)


def do_select(data, q, idx=0):
    ret = []

    key = q[idx]

    for datakey,value in iterate(data):

        if len(q) == idx+1:
            if not type_check(value, key['type']):
                if is_iterable(value):
                    ret.extend(do_select(value, q, idx))
                continue

            if key['name'] and datakey != key['name']:
                if is_iterable(value):
                    ret.extend(do_select(value, q, idx))
                continue

            ret.append(value)
        else:
            if not is_iterable(value):
                continue
            if datakey == key['name'] or (not key['name']
                                          and type_check(value, key['type'])):
                ret.extend(do_select(value, q, idx + 1))
            else:
                ret.extend(do_select(value, q, idx))
    return ret


def select(data, query_string):
    q = parse_query(query_string)
    return do_select(data, q)


def argparser():
    import argparse
    from sys import stdin, stdout
    argp = argparse.ArgumentParser(description='ds - Simple data query language')
    argp.add_argument('-o', '--output'
                     ,help      = 'Output file - default is STDOUT'
                     ,metavar   = 'FILE'
                     ,default   = stdout
                     ,type      = argparse.FileType('w')
                     )
    argp.add_argument('-i', '--input'
                     ,help      = 'Input file - default is STDIN'
                     ,metavar   = 'FILE'
                     ,default   = stdin
                     ,type      = argparse.FileType('r')
                     )
    argp.add_argument('-f', '--format'
                     ,help      = 'Input format - default is JSON'
                     ,metavar   = 'FORMAT'
                     ,default   = 'JSON'
                     )
    argp.add_argument('query'
                     ,metavar   = 'QUERY'
                     ,help      = 'query string'
                     )
    return vars(argp.parse_args())


def __main__():
    from sys import exit, stderr
    args = argparser()

    supported_formats = ('JSON', 'pickle')

    if args['format'] not in supported_formats:
        stderr.write('[E] not supported format: {0}'.format(args['format']))
        exit(1)

    if args['format'] == 'JSON':
        from json import load
    elif args['format'] == 'pickle':
        from pickle import load

    d = load(args['input'])

    for result in select(d, args['query']):
        args['output'].write('{0}\n'.format(result.encode('utf-8')))


if __name__ == '__main__':
    __main__()
