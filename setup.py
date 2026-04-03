from setuptools import setup, find_packages

setup(
    name="imageforge",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["main"],
    install_requires=[
        "click >= 8.3.1",
        "Pillow >= 12.1.1",
    ],
    entry_points={
        "console_scripts": [
            "imageforge=main:cli"
        ]
    }
)
