import setuptools
from EmailSMS import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='emailSMS-python',
    version=1.0,

    url='https://github.com/JoeWomelsdorf/Python_Email2SMS',
    author='Joe Womelsdorf',
    author_email='josef.womelsdorf@outlook.com',
    packages=setuptools.find_packages(),
    description="An email to sms gateway for Python3",
         classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],


    py_modules=['my_pip_package'],
)