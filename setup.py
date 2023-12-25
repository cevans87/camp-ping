from pathlib import Path
from setuptools import find_packages, setup

setup(
    description='Cancellation monitor for various reservation websites.',
    entry_points={
        'console_scripts': ['camp-ping=__main__:main']
    },
    name='camp-ping',
    packages=find_packages(exclude=('test',)),
    python_requires='>=3.9',
    extras_require={
        'base': (base := [
            *filter(None, (Path(__file__).parent / 'pip_requirements.txt').read_text().splitlines())
        ]),
        'test': (test := base + [
            *filter(None, (Path(__file__).parent / 'test' / 'pip_requirements.txt').read_text().splitlines())
        ]),
    },
    install_requires=base,
    url='https://github.com/cevans87/camp-ping',
    version='0.0.1',
)
