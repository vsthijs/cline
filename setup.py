from setuptools import setup

setup(
    name="cline",
    version="0.0.1",
    entry_points={"console_scripts": ["cline=cline.__main__:main"]},
)
