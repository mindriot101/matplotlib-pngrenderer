from setuptools import setup
import os

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
        name='pngrenderer',
        version='0.1.0',
        description='Render matplotlib png images to a zip file',
        author='Simon Walker',
        license=read('LICENSE'),
        author_email='s.r.walker101@gmail.com',
        url='http://example.com',
        packages=['pngrenderer',],
        install_requires=['matplotlib'],
        long_description=read('README.markdown'),
        )
