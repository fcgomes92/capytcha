from setuptools import setup


def _get_version():
    with open('VERSION') as fd:
        return fd.read().strip()


setup(
    name='capytcha',
    version=_get_version(),
    packages=['capytcha'],
    package_dir={'': './'},
    py_modules=['capytcha.app'],
    entry_points={
        'console_scripts': [
            'capytcha-serve=capytcha.app:main',
        ]
    }
)
