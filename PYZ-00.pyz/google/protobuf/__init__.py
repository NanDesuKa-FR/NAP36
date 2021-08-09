# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\google\protobuf\__init__.py
__version__ = '3.6.1'
if __name__ != '__main__':
    try:
        __import__('pkg_resources').declare_namespace(__name__)
    except ImportError:
        __path__ = __import__('pkgutil').extend_path(__path__, __name__)