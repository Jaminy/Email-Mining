import distutils.core
import sys
# Importing setuptools adds some features like "setup.py test", but
# it's optional so swallow the error if it's not there.
try:
    import setuptools
except ImportError:
    pass

major, minor = sys.version_info[:2]
python_25 = (major > 2 or (major == 2 and minor >= 5))
if not python_25:
    raise RuntimeError("Python 2.5 or newer is required")

# Add ./python/ subdirectory to path
sys.path.append('python')

# Discover version of phonenumbers package
from phonenumbers import __version__

distutils.core.setup(name='phonenumbers',
                     version=__version__,
                     description="Python version of Google's common library for parsing, formatting, storing and validating international phone numbers.",
                     author='David Drysdale',
                     author_email='dmd@lurklurk.org',
                     url='https://github.com/daviddrysdale/python-phonenumbers',
                     license='Apache License 2.0',
                     packages=['phonenumbers', 'phonenumbers.data', 'phonenumbers.geodata', 'phonenumbers.shortdata',
                               'phonenumbers.carrierdata', 'phonenumbers.tzdata'],
                     package_dir={'': 'python'},
                     test_suite="tests.examplenumberstest",
                     platforms='Posix; MacOS X; Windows',
                     classifiers=['Development Status :: 5 - Production/Stable',
                                  'Intended Audience :: Developers',
                                  'License :: OSI Approved :: Apache Software License',
                                  'Operating System :: OS Independent',
                                  'Topic :: Communications :: Telephony',
                                  'Programming Language :: Python :: 2',
                                  'Programming Language :: Python :: 2.5',
                                  'Programming Language :: Python :: 2.6',
                                  'Programming Language :: Python :: 2.7',
                                  'Programming Language :: Python :: 3',
                                  ],
                     )
