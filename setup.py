import os
from setuptools import setup, find_packages

requires = [
    'setuptools',
    'PIL',
    'ptah >= 0.2.1',
    ]


setup(name='ploud.themegallery',
      version='0.1dev',
      description='ploud theme gallery',
      classifiers=[
          "Programming Language :: Python",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
          ],
      author='Nikolay Kim, Enfold Systems Inc',
      author_email='fafhrd91@gmail.com',
      url='',
      keywords='web wsgi ptah',
      packages=find_packages(),
      namespace_packages=['ploud'],
      include_package_data=True,
      zip_safe=False,
      install_requires = requires,
      entry_points = {
          'paste.app_factory': [
              'main = ploud.themegallery.app:main'],
          },
      )
