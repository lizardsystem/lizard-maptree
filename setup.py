from setuptools import setup

version = '1.9'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('TODO.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'Django',
    'django-staticfiles',
    'django-extensions',
    'lizard-ui >= 4.0, < 5.0',
    'lizard-map >= 4.0, < 5.0',
    'django-nose',
    'pkginfo',
    'django-treebeard',
    'factory_boy'
    ],

tests_require = [
    ]

setup(name='lizard-maptree',
      version=version,
      description="Provides tree view functionality to lizard-map applications. ",
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Programming Language :: Python',
                   'Framework :: Django',
                   ],
      keywords=[],
      author='Jack Ha',
      author_email='jack.ha@nelen-schuurmans.nl',
      url='',
      license='GPL',
      packages=['lizard_maptree'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require = {'test': tests_require},
      entry_points={
          'console_scripts': [
          ]},
      )
