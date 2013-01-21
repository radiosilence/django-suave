from setuptools import setup, find_packages

requires = []
dep_links = []

for dep in open('requirements.txt').read().split("\n"):
    if dep.startswith('git+'):
        dep_links.append(dep)
    else:
        requires.append(dep)

setup(
    name='django-suave',
    version="0.5.14",
    description='Rather nice pages.',
    long_description=open('README.rst').read(),
    url='https://github.com/radiosilence/django-suave',
    author='James Cleveland',
    author_email='jamescleveland@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    license="LICENSE.txt",
    install_requires=requires,
    dependency_links=dep_links,
)
