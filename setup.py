
from setuptools import setup

setup(
    name="tap-15five",
    version="0.1.0",
    description="Singer.io tap for extracting data",
    author="Stitch",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_15five"],
    install_requires=[
        "singer-python>=5.0.12",
        "requests",
    ],
    entry_points="""
    [console_scripts]
    tap-15five=tap_15five:main
    """,
    packages=["tap_15five"],
    package_data = {
        "schemas": ["tap_15five/schemas/*.json"]
    },
    include_package_data=True,
)
