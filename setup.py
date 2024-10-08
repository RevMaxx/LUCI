from setuptools import setup, find_packages

with open("readme.mD", "r") as fh:
    long_description = fh.read()

setup(
    name="LuciAI",
    version="0.5.0",
    description='The First AI-Based Medical Agent Designed to Automate All Medical Processes.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        "cerina",
        "openai",
        "together",
        "langchain",
        "langchain-together",
        "langchain-core",
        "langchain-community",
        "ijson",
        "pydantic",
        "gradio",
        "speechrecognition",
        "biopython",
        "pyyaml"
    ],
    author="wbavishek",
    author_email="wbavishek@gmail.com",
    url="https://revmaxx.co",  
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,  
    package_data={
       'logo': ['*.png'],  
    },
    entry_points={
        'console_scripts': [
            'luci-cli = Luci.cli:main',  # luci-cli will be the command to run
        ],
    },
)
