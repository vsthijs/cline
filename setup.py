from setuptools import setup
from cline import __VERSION__ as version

setup(
    name="cline",
    version=version,
    entry_points={"console_scripts": ["cline=cline.__main__:main"]},
)
