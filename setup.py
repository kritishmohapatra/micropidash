from setuptools import setup, find_packages

setup(
    name="micropidash",
    version="1.0.0",
    description="A lightweight web dashboard for MicroPython (ESP32, Pico W)",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Kritish Mohapatra",
    author_email="kritishmohapatra06norisk@gmail.com",
    url="https://github.com/kritishmohapatra/micropidash",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
