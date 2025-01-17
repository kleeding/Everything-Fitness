from setuptools import setup, find_packages

setup(
    name="Everything Fitness",
    version="0.1",
    description="A fitness and nutrition tracking app",
    author="Kent Leeding",
    packages=find_packages(where="everything_fitness"),
    package_dir={"": "everything_fitness"},
)