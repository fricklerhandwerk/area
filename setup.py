"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['area/gui.py']
NAME = "Area"
VERSION = "0.1.1"
DESC = "A simple two-player round-based tactics game"
LONG_DESC = "Two players occupy board area by changing their field's color. The player who captured more than half the board wins."
DATA_FILES = []
OPTIONS =	{
         		'argv_emulation': True,
                'iconfile': 'img/icon.icns',
                'plist':
                {
                    'CFBundleName': NAME,
                    'CFBundleDisplayName': NAME,
                    'CFBundleVersion': VERSION,
                    'CFBundleShortVersionString': VERSION,
                }
            }


setup(
	name=NAME,
    app=APP,
    version=VERSION,
    description=DESC,
    long_description=LONG_DESC,
    author="frickler01",
    maintainer="frickler01",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Topic :: Games/Entertainment'
        ],
    license='MIT License',
    platform='POSIX',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
