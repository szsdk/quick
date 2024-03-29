from setuptools import setup

setup(
    name="quick",
    version="1.0",
    description="Draw qt gui for click script",
    author="Shen Zhou",
    author_email="shenz34206@hotmail.com",
    license="GNU GPLv3",
    py_modules=["quick"],
    install_requires=["click>=6.5", "qtpy"],
    extras_require={"qtstyle": ["qdarkstyle"]},
)
