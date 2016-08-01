# coding:utf-8
from setuptools import setup

setup(
    name = 'pybilibili',
    version = '0.1',
    packages = ['pybilibili'],
    requires = ['requests', 'bs4', 'colorama'],
    url = 'http://www.iamsss.com/',
    license = 'BSD',
    author = 'Shi Shushun',
    author_email = 'shiss2001@outlook.com',
    description = 'A Console tool for Bilibili'
    )