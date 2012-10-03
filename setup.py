from setuptools import setup, find_packages

setup(
    name='django-suave',
    version="0.4.1",
    description='Rather nice pages.',
    long_description=open('README.rst').read(),
    url='https://github.com/radiosilence/django-suave',
    author='James Cleveland',
    author_email='jamescleveland@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    license="LICENSE.txt",
    install_requires=open('requirements.txt').read().split("\n")
)
