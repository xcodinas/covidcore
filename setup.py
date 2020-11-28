import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="CovidCoreApi",
    version="0.0.1",
    author="Xavier Codinas",
    author_email="xavier19966@gmail.com",
    description=("Api for CovidCore."),
    license="BSD",
    packages=['app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'Flask-sqlalchemy',
        'Flask-migrate',
        'Flask-script',
        'Flask-restful',
        'Flask-jwt-extended',
        'Flask-mail',
        'Flask-Babelex',
        'passlib',
        'psycopg2',
        'PyMySQL',
    ],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    test_suite='tests',
)
