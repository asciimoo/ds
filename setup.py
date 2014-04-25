from setuptools import setup, find_packages

setup(
    name = 'ds',
    version = '0.0.1',
    author = 'Adam Tauber',
    author_email = 'asciimoo@gmail.com',
    description = ('Simple data query language'),
    license = 'AGPLv3+',
    keywords = "data query",
    url = 'https://github.com/asciimoo/ds',
    scripts = ['ds.py'],
    py_modules = ['ds'],
    packages = find_packages(),
    install_requires = [],
    download_url = 'https://github.com/asciimoo/ds/tarball/master',
    entry_points={
        "console_scripts": ["ds=ds:__main__"]
    },
    classifiers = [
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        'Environment :: Console',
        'License :: OSI Approved :: GNU Affero General Public License v3'
    ],
)
