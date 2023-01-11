from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-cookies-for-magic-parameters",
    description="UI for setting cookies to populate magic parameters",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-cookies-for-magic-parameters",
    project_urls={
        "Issues": "https://github.com/simonw/datasette-cookies-for-magic-parameters/issues",
        "CI": "https://github.com/simonw/datasette-cookies-for-magic-parameters/actions",
        "Changelog": "https://github.com/simonw/datasette-cookies-for-magic-parameters/releases",
    },
    license="Apache License, Version 2.0",
    classifiers=[
        "Framework :: Datasette",
        "License :: OSI Approved :: Apache Software License",
    ],
    version=VERSION,
    packages=["datasette_cookies_for_magic_parameters"],
    entry_points={
        "datasette": [
            "cookies_for_magic_parameters = datasette_cookies_for_magic_parameters"
        ]
    },
    install_requires=["datasette"],
    extras_require={"test": ["pytest", "pytest-asyncio"]},
    python_requires=">=3.7",
)
