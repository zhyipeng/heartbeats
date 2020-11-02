import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="heartbeats",
    version="0.0.1",
    author="zhyipeng",
    author_email="zhyipeng@outlook.com",
    description="Check heartbeats by method called.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhyipeng/heartbeats",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
