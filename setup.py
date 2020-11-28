import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="covidcore",
    version="0.1.0",
    author="Xavier Codinas",
    author_email="xavier19966@gmail.com",
    description=("An app with flask"),
    license="BSD",
    packages=['covidcore'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'Flask-login',
        'Flask-sqlalchemy',
        'Flask-migrate',
        'Flask-security-too',
        'Flask-script',
        'Flask-admin==1.5.2',
        'Flask-Babelex',
        'Wtforms',
        'setuptools==39.2.0',
        'sentry-sdk[flask]==0.8.0',
        'python-magic',
    ],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    test_suite='tests',
)
