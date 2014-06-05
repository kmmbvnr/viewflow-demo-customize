#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup


setup(
    name='django-travel-demo',
    version='0.1.0',
    author='Mikhail Podgurskiy',
    author_email='kmmbvnr@gmail.com',
    description='Travel Request Approval Workflow',
    platforms=['Any'],
    keywords=['workflow', 'django'],
    classifiers=[
        'Development Status :: 3 - Alpha',
    ],
    requires=['Django (>=1.7b1)'],
    packages=['travel',],
)
