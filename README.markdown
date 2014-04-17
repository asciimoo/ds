ds
=========

Simple data query "language"


### Examples

```python
from ds import select

data = {'a': 1,
        'b': [2, 3, {'ba': 4.0,
                     'bb': {'bba': 5,
                            'a': 'z'}}],
        'c': 7,
        'd': [2, 3, {'ba': True}]}

select(data, '/a')  # [1, 'z']
select(data, '/bb/a')  # ['z']
select(data, '/b/0')  # [2]
select(data, '/b/<float>')  # [4.0]
select(data, '/<str>a')  # ['z']
select(data, '/ba')  # [4.0, True]
```

see `ds --help` for command line usage

```bash
# by default ds accepts JSON format from standard input
$ echo '{"a": [1, 2], "b": "c"}' | ds /b
c

# using pickle as input
$ ds -t pickle -i file.pickle /query
```

### Installation

To install ds, simply:

```bash
$ pip install ds
```

or

```bash
$ easy_install ds
```


### Bugs

Bugs or suggestions? Visit the [issue tracker](https://github.com/asciimoo/ds/issues).


### License

```
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
```
