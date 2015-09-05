from distutils.core import setup
from setuptools import find_packages

setup(
    name='op.backend',
    version='0.0.0',
    author='Darwin Monroy',
    author_email='contact@darwinmonroy.com',
    namespace_packages=['op'],
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/dmonroy/op.backend',
    description='Access and manage the Open PaaS data backend',
    install_requires=[
        'op.common'
    ],
)
