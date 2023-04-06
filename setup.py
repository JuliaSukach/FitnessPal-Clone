import pathlib
from setuptools import setup, find_packages

BASE_DIR = pathlib.Path(__file__).parent.absolute()


def get_version():
    with open(BASE_DIR / 'VERSION') as file:
        return file.readline().strip()


def get_license():
    with open(BASE_DIR / 'LICENSE') as file:
        return file.read().strip()


def get_desc():
    with open(BASE_DIR / 'README.md') as file:
        return file.read().strip()


def get_packages():
    with open(BASE_DIR / 'requirements.txt') as file:
        return [package.strip() for package in file if package or not package.startswith('#')]


setup(
    name='fitnessapp',
    version=get_version(),
    author='Yulia',
    author_email='yuliyasukach123@gmail.com',
    url='https://github.com/YuliaSukach/diploma-project',
    packages=find_packages('.', include=['fitnessapp'], exclude=['*tests*.py', 'test*']),
    package_dir={'': '.'},
    include_package_data=True,
    license=get_license(),
    description='This is a fitness app',
    long_description=get_desc(),
    long_description_content_type='text/markdown',
    install_requires=get_packages(),
    python_required='≥3.10',
    classifiers=[
        'Development Status :: 3 - Alpha'
        if 'dev' in get_version()
        else 'Development Status :: 4 Beta'
        if 'rc' in get_version()
        else 'Development Status :: 5 Production/Stable'
    ]
)
