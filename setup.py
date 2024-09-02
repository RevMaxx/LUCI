from setuptools import setup, find_packages

with open("readme.mD", "r") as fh:
    long_description = fh.read()

setup(
    name="Luci",
    version="0.0.1",
    description='The First AI-Based Medical Agent Designed to Automate All Medical Processes.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        "cerina",
        "openai",
    ],
)