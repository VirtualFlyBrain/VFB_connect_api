from setuptools import setup, find_packages

setup(
    name='vfb_connect_api',
    version='1.0.0',
    description='VFB_connect restful API that wraps data/knowledgeBase query endpoints and returns VFB_json',
    url='https://github.com/VirtualFlyBrain/VFB_connect_api',
    author='Huseyin Kir',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Virtual Fly Brain',
        'License :: Apache License Version 2.0',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='rest flask swagger flask-restplus virtual-fly-brain vfb_connect',

    packages=find_packages(),

    install_requires=['flask-restplus==0.13', 'vfb_connect'],
)
