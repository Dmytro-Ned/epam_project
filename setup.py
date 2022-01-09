"""
A setup file with configurations.
"""

from setuptools import setup, find_packages

setup(
    name='snaketests',
    version='1.0',
    author='jagdpanther',
    author_email='dmtr.ned@gmail.com',
    description='Web application with Python quizzes',
    url='https://github.com/Dmytro-Ned/epam_project',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
