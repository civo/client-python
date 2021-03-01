import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="civo",
    version="1.0.8",
    url="https://github.com/civo/client-python",
    license='MIT License',
    author="Alejandro JNM",
    author_email="alejandrojnm@gmail.com",
    description="Wrapper for civo api",
    long_description=read("civo/README.rst"),
    packages=find_packages(exclude=('tests',)),
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
