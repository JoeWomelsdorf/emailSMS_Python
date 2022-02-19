from setuptools import setup
from EmailSMS import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='emailSMS-python',
    version=1.0,

    url='https://github.com/JoeWomelsdorf/Python_Email2SMS',
    author='Joe Womelsdorf',
    author_email='josef.womelsdorf@outlook.com',
    description="An email to sms gateway for Python3",

    py_modules=['my_pip_package'],
)