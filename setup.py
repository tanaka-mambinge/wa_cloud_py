from setuptools import find_packages, setup

setup(
    name="wa_cloud_py",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests>=2.26.0", "loguru>=0.7.0"],
    author="Tanaka Mambinge",
    author_email="tmambingez@gmail.com",
    description="A Python library for sending WhatsApp messages using the WhatsApp Cloud API",
    download_url="https://github.com/tanaka-mambinge/chatterbox/archive/refs/tags/v_01.tar.gz",
)
